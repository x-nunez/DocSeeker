# SPDX-License-Identifier: Apache-2.0

import os
import requests
from urllib.parse import urlencode
from fastapi import APIRouter, Request, HTTPException, BackgroundTasks
from fastapi.responses import RedirectResponse, JSONResponse
from src.eater.eater import recibir_documento
from src.db.interfazDB import crearCollection
from src.classes.document import Document
from src.cloud.file import File
from src.cloud.googleDrive import checkFile
from datetime import datetime


# Read .env parameters for connection
CLIENT_ID = os.getenv("MICROSOFT_CLIENT_ID")
CLIENT_SECRET = os.getenv("MICROSOFT_CLIENT_SECRET")
REDIRECT_URI = os.getenv("MICROSOFT_REDIRECT_URI")
TENANT_ID = os.getenv("MICROSOFT_TENANT_ID", "common")  # 'common' para cuentas personales y de empresa
SCOPE = "Files.Read.All User.Read offline_access"
GRAPH_BASE = "https://graph.microsoft.com/v1.0"

router = APIRouter()

#Tipos MIME de OneDrive que no se pueden/quieren procesar

SKIP_MIME_TYPES = {
    "application/vnd.microsoft.team.message",
    "application/vnd.microsoft.team.giphyextension",
    "image/jpeg",
    "image/png",
    "image/gif",
    "image/bmp",
    "image/webp",
    "video/mp4",
    "video/quicktime",
    "audio/mpeg",
    "audio/wav",
    "application/octet-stream",
}

# Tipos MIME nativos de Office que se exportan como texto plano
OFFICE_TO_TEXT = {
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    "application/msword",
    "application/vnd.ms-excel",
    "application/vnd.ms-powerpoint"
}


#Helpers de descarga

def _auth_headers(access_token):
    return {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json"
    }

def getBinaryFile(access_token, file_id):
    """Descarga un archivo binario directamente desde OneDrive."""
    url = f"{GRAPH_BASE}/me/drive/items/{file_id}/content"
    return requests.get(url, headers=_auth_headers(access_token), stream=True, allow_redirects=True)

def getOfficeFileAsText(access_token, file_id):
    """
    Convierte un archivo Office a PDF mediante la API de conversión de OneDrive
    y luego lo descarga. Para texto plano se puede usar la vista previa de texto
    si está disponible; aquí usamos la descarga directa del archivo original
    y delegamos la extracción de texto al eater.
    """
    # OneDrive no exporta a texto plano como Google Drive, así que descargamos
    # el binario original y dejamos que el eater lo procese (docx, xlsx, pptx).
    return getBinaryFile(access_token, file_id)


def getFile(access_token, file_metadata):
    """
    Dado el metadata de un item de OneDrive, descarga el archivo y
    devuelve un objeto File. Devuelve None si el tipo debe ignorarse.
    """
    file_id   = file_metadata["id"]
    file_name = file_metadata["name"]
    mime_type = file_metadata.get("file", {}).get("mimeType", "")

    # Ignorar carpetas (no tienen la clave "file")
    if "folder" in file_metadata:
        return None

    # Ignorar tipos que no queremos procesar
    if mime_type in SKIP_MIME_TYPES:
        return None

    response = getBinaryFile(access_token, file_id)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    os.makedirs("tmp", exist_ok=True)
    file_path = os.path.join("tmp", file_name)

    with open(file_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)

    return File(file_path, file_name, file_metadata)


def updateDB(access_token):
    url = f"{GRAPH_BASE}/me/drive/root/delta"
    headers = _auth_headers(access_token)

    while url:
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.text
            )
        data = response.json()

        for f in data.get("value", []):

            if "folder" in f or "file" not in f:
                continue

            mime_type = f.get("file", {}).get("mimeType", "")
            file_id = f.get("id")
            file_name = f.get("name")

            if mime_type in SKIP_MIME_TYPES:
                continue

            try:
                if mime_type in OFFICE_TO_TEXT:
                    download_url = f"{GRAPH_BASE}/me/drive/items/{file_id}/content?format=pdf"
                    response_file = requests.get(
                        download_url,
                        headers=headers,
                        stream=True
                    )
                    file_name = file_name.rsplit(".", 1)[0] + ".pdf"
                else:
                    response_file = getBinaryFile(access_token, file_id)

                if response_file.status_code != 200:
                    print("Download failed:", file_name, response_file.text)
                    continue

                os.makedirs("tmp", exist_ok=True)
                file_path = os.path.abspath(os.path.join("tmp", file_name))

                if checkFile(file_path):
                    continue

                with open(file_path, "wb") as out:
                    for chunk in response_file.iter_content(chunk_size=8192):
                        if chunk:
                            out.write(chunk)

                extension = os.path.splitext(file_name)[1].lstrip(".") or ""

                created = datetime.fromisoformat(f.get("createdDateTime").replace("Z", "+00:00"))
                modified = datetime.fromisoformat(f.get("lastModifiedDateTime").replace("Z", "+00:00"))

                documento = Document(
                    file_path,
                    file_name,
                    extension,
                    modified,
                    created,
                    f.get("size"),
                    f.get("webUrl")
                )

                try:
                    recibir_documento(documento)
                except Exception as e:
                    print("Processing failed:", file_name, e)

            except Exception as e:
                print("Unexpected error:", file_name, e)

        url = data.get("@odata.nextLink")

#Rutas OAuth2

@router.get("/auth/microsoft/login")
def login_with_microsoft():
    print("CLIENT_ID: ", CLIENT_ID)
    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPE,
        "response_mode": "query",
        "prompt": "consent"
    }
    url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/authorize?{urlencode(params)}"
    return RedirectResponse(url)


@router.get("/auth/microsoft/callback")
def microsoft_callback(request: Request, code: str = None, background_tasks: BackgroundTasks = None):
    if not code:
        return JSONResponse({"error": "No code provided"}, status_code=400)
    print("CLIENT_SECRET: ", CLIENT_SECRET)
    token_url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
    data = {
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
        "scope": SCOPE
    }

    r = requests.post(token_url, data=data)
    token_response = r.json()
    print("TOKEN RESPONSE: ", token_response)

    onedrive_token = token_response.get("access_token")
    expires_in   = int(token_response.get("expires_in", 3600))

    if not onedrive_token:
        return JSONResponse({"error": "No access token returned"}, status_code=400)

    response = RedirectResponse(url="http://localhost:3000/dashboard")
    response.set_cookie(
        key="onedrive_token",
        value=onedrive_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=expires_in
    )

    if background_tasks:
        background_tasks.add_task(crearCollection)
        background_tasks.add_task(updateDB, onedrive_token)

    return response


@router.get("/downloadall/microsoft")
def downloadall(request: Request):
    onedrive_token = request.cookies.get("onedrive_token")
    updateDB(onedrive_token)


@router.get("/auth/microsoft/me")
def me(request: Request):
    onedrive_token = request.cookies.get("onedrive_token")
    print("Cookie = ", onedrive_token)

    if not onedrive_token:
        raise HTTPException(status_code=401, detail="Missing token")

    # Perfil del usuario
    userinfo_resp = requests.get(
        f"{GRAPH_BASE}/me",
        headers=_auth_headers(onedrive_token),
        timeout=15
    )
    if userinfo_resp.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    # Info del drive (quota, etc.)
    drive_resp = requests.get(
        f"{GRAPH_BASE}/me/drive",
        headers=_auth_headers(onedrive_token),
        timeout=15
    )
    if drive_resp.status_code != 200:
        raise HTTPException(status_code=400, detail="OneDrive API request failed")

    return JSONResponse(
        status_code=200,
        content={
            "profile": userinfo_resp.json(),
            "drive": drive_resp.json(),
        }
    )


@router.get("/auth/microsoft/logout")
def logout():
    response = JSONResponse({"message": "Logged out successfully"})
    response.delete_cookie(key="onedrive_token", path="/")
    return response