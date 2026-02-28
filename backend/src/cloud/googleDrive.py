import os
import re
import requests
from urllib.parse import urlencode
from fastapi import APIRouter, Request, HTTPException, BackgroundTasks
from fastapi.responses import RedirectResponse, JSONResponse
from src.db.interfazDB import crearCollection

from src.cloud.file import File

# Read .env parameters for connection
CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
SCOPE = "https://www.googleapis.com/auth/drive openid email profile"

router = APIRouter()

def getBinaryFile(access_token, file_id):
	headers = {
		"Authorization": f"Bearer {access_token}"
	}
	url = f"https://www.googleapis.com/drive/v3/files/{file_id}"
	params = {
		"alt": "media",
		"fields": "files(*)"
	}
	return requests.get(url, headers=headers, params=params, stream=True)

def getDocumentFile(access_token, file_id):
	headers = {
		"Authorization": f"Bearer {access_token}"
	}
	url = f"https://www.googleapis.com/drive/v3/files/{file_id}/export"
	params = {
		"mimeType": "text/plain",
		"fields": "files(*)"
	}
	return requests.get(url, headers=headers, params=params, stream=True)

def getSheetFile(access_token, file_id):
	headers = {
		"Authorization": f"Bearer {access_token}"
	}
	url = f"https://www.googleapis.com/drive/v3/files/{file_id}/export"
	params = {
		"mimeType": "text/csv",
		"fields": "files(*)"
	}
	return requests.get(url, headers=headers, params=params, stream=True)

def getPresentationsFile(access_token, file_id):
	headers = {
		"Authorization": f"Bearer {access_token}"
	}
	url = f"https://www.googleapis.com/drive/v3/files/{file_id}/export"
	params = {
		"mimeType": "text/plain",
		"fields": "files(*)"
	}
	return requests.get(url, headers=headers, params=params, stream=True)

def getDrawingsFile(access_token, file_id):
	headers = {
		"Authorization": f"Bearer {access_token}"
	}
	url = f"https://www.googleapis.com/drive/v3/files/{file_id}/export"
	params = {
		"mimeType": "image/png",
		"fields": "files(*)"
	}
	return requests.get(url, headers=headers, params=params, stream=True)

def getFile(access_token, file_metadata):
	file_id = file_metadata['id']
	file_name = file_metadata['name']
	file_mimeType = file_metadata['mimeType']

	if file_mimeType in ["application/vnd.google-apps.folder", "application/vnd.google-apps.audio", "application/vnd.google-apps.drive-sdk", "application/vnd.google-apps.form", "application/vnd.google-apps.fusiontable", "application/vnd.google-apps.jam", "application/vnd.google-apps.mail-layout", "application/vnd.google-apps.map", "application/vnd.google-apps.script", "application/vnd.google-apps.shortcut", "application/vnd.google-apps.site",
					  "application/vnd.google-apps.photo", "application/vnd.google-apps.vid", "application/vnd.google-apps.video"]:
		return
	elif file_mimeType == "application/vnd.google-apps.drawing":
		response = getDrawingsFile(access_token, file_id)
		file_name = file_name + ".png"
	elif file_mimeType == "application/vnd.google-apps.presentation":
		response = getPresentationsFile(access_token, file_id)
		file_name = file_name + ".txt"
	elif file_mimeType == "application/vnd.google-apps.spreadsheet":
		response = getSheetFile(access_token, file_id)
		file_name = file_name + ".txt"
	elif file_mimeType in "application/vnd.google-apps.document":
		response = getDocumentFile(access_token, file_id)
		file_name = file_name + ".txt"
	else:
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

def checkFile(file_metadata):
	return True


def updateDB(access_token):
	files = []

	headers = {
		"Authorization": f"Bearer {access_token}",
		"Accept": "application/json"
	 }
	url = "https://www.googleapis.com/drive/v3/files"
	params = {
		"pageSize": 1000,              # máximo por página
		"fields": "nextPageToken,files(*)"
	}
	while True:
		response = requests.get(url, headers=headers, params=params)
		if response.status_code != 200:
			# si hay error de autorización o token inválido
			raise HTTPException(status_code=response.status_code, detail=response.text)
		data = response.json()
		files.extend(data.get("files", []))
		next_token = data.get("nextPageToken")
		if not next_token:
			break
		params["pageToken"] = next_token

	for f in files:
		print(f)
		if checkFile(f):
			file = getFile(access_token, f)
			documento = documento(file.name, file.path, file.metadata["fileExtension"])
			# id = insertarPostgreSQL(documento)
			

	return

# Login Endpoint
@router.get("/auth/google/login")
def login_with_google():
    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "scope": SCOPE,
        "redirect_uri": REDIRECT_URI,
        "access_type": "offline",
        "prompt": "consent"
    }
    url = f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}"
    return RedirectResponse(url)

# Google login callback
@router.get("/auth/google/callback")
def google_callback(request: Request, code: str = None, background_tasks: BackgroundTasks = None):
    if not code:
        return JSONResponse({"error": "No code provided"}, status_code=400)

    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code"
    }

    r = requests.post(token_url, data=data)
    token_response = r.json()

    access_token = token_response.get("access_token")
    expires_in = int(token_response.get("expires_in", 3600))

    if not access_token:
        return JSONResponse({"error": "No access token returned"}, status_code=400)

    response = RedirectResponse(url=f"http://localhost:3000/dashboard")
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=expires_in
	)

    if background_tasks:
        background_tasks.add_task(crearCollection)
        background_tasks.add_task(updateDB, access_token)
    return response

@router.get("/downloadall/google")
def downloadall(request: Request):
    access_token = request.cookies.get("access_token")

    if not access_token:
        raise HTTPException(status_code=401, detail="Missing token")

    files = []

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json"
    }
    url = "https://www.googleapis.com/drive/v3/files"
    params = {
        "pageSize": 1000,
        "fields": "nextPageToken,files(id,name,mimeType)"
    }

    while True:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)

        data = response.json()
        files.extend(data.get("files", []))

        next_token = data.get("nextPageToken")
        if not next_token:
            break
        params["pageToken"] = next_token
    print(files)
    return "Test"

@router.get("/auth/google/me")
def me(request: Request):
    access_token = request.cookies.get("access_token")
    print("Cookie = ", access_token)

    if not access_token:
        raise HTTPException(status_code=401, detail="Missing token")

    userinfo_resp = requests.get(
        "https://openidconnect.googleapis.com/v1/userinfo",
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=15
    )
    if userinfo_resp.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    drive_resp = requests.get(
        "https://www.googleapis.com/drive/v3/about?fields=user,storageQuota",
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=15
    )
    if drive_resp.status_code != 200:
        raise HTTPException(status_code=400, detail="Drive API request failed")

    return JSONResponse(
        status_code=200,
        content={
            "profile": userinfo_resp.json(),
            "drive": drive_resp.json(),
        },
    )

@router.get("/auth/google/logout")
def logout():
    response = JSONResponse({"message": "Logged out successfully"})
    response.delete_cookie(key="access_token", path="/")
    return response