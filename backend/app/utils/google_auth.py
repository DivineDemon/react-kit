import os

from dotenv import load_dotenv
from fastapi import HTTPException
from google.auth.transport import requests
from google.oauth2 import id_token

load_dotenv()

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")


def verify_google_token(token: str):

  try:
    idinfo = id_token.verify_oauth2_token(token, requests.Request(),
                                          GOOGLE_CLIENT_ID)
    if idinfo["aud"] != GOOGLE_CLIENT_ID:
      raise ValueError("Could not verify audience.")

    return {
        "email": idinfo["email"],
        "name": idinfo.get("name", ""),
        "picture": idinfo.get("picture", ""),
        "sub": idinfo["sub"],  # Google user ID
    }
  except ValueError as e:
    raise ValueError(f"Invalid Google token: {e}")


def get_user_info_from_access_token(access_token: str):
  url = "https://www.googleapis.com/oauth2/v1/userinfo"
  headers = {"Authorization": f"Bearer {access_token}"}
  response = requests.get(url, headers=headers)

  if response.status_code != 200:
    raise HTTPException(status_code=400,
                        detail="Failed to fetch user info from Google")

  return response.json()
