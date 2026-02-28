from dotenv import load_dotenv
load_dotenv('.env')
from fastapi import FastAPI
from src.cloud.googleDrive import app

# Redirect to Google login
@app.get("/auth/google/login")
def login():
    return login_with_google()

# Handle callback from Google
@app.get("/auth/google/callback")
def callback(code: str = None):
    return google_callback(code)
