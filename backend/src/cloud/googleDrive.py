import os
import requests
from urllib.parse import urlencode
from fastapi import FastAPI
from fastapi import Request, HTTPException, APIRouter
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Read .env parameters for connection
CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
SCOPE = "https://www.googleapis.com/auth/drive openid email profile"

# Login Endpoint
@app.get("/auth/google/login")
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
@app.get("/auth/google/callback")
def google_callback(request: Request, code: str = None):
	if not code:
		return JSONResponse({"error": "No code provided"}, status_code=400)

	# Exchange code for tokens
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

	response = RedirectResponse(
        url=f"http://localhost:3000/dashboard"
    )
	response.set_cookie(
		key="access_token",
		value=access_token,
		httponly=True,
		secure=False,
		samesite="lax",
		max_age=expires_in
	)

	return response

@app.get("/downloadall/google")
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
		"pageSize": 1000,              # máximo por página
		"fields": "nextPageToken,files(id,name,mimeType)"
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
	print(files)
	return "Test"

@app.get("/auth/google/me")
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