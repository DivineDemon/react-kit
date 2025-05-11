import os

import requests
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2 import id_token

load_dotenv()

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USER_INFO_URL = "https://www.googleapis.com/oauth2/v1/userinfo"


class GoogleAuthService:

  @staticmethod
  def get_google_auth_url():
    """
        Generate Google OAuth URL for authentication.
        """
    auth_url = (f"https://accounts.google.com/o/oauth2/v2/auth?"
                f"response_type=code&"
                f"client_id={GOOGLE_CLIENT_ID}&"
                f"redirect_uri={GOOGLE_REDIRECT_URI}&"
                f"scope=email profile")
    return auth_url

  @staticmethod
  def exchange_code_for_tokens(code: str):
    """
        Exchange the authorization code for access and ID tokens.
        """
    token_url = "https://oauth2.googleapis.com/token"
    payload = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
        "redirect_uri": os.getenv("GOOGLE_REDIRECT_URI"),
        "grant_type": "authorization_code",
    }
    response = requests.post(token_url, data=payload)

    if response.status_code != 200:
      raise Exception("Failed to fetch tokens")

    return response.json()

  @staticmethod
  def get_user_info(id_token_str: str):
    """
        Get user information from the ID token.
        """
    try:
      id_info = id_token.verify_oauth2_token(id_token_str, Request(),
                                             GOOGLE_CLIENT_ID)

      return {
          "email": id_info["email"],
          "name": id_info.get("name", ""),
          "picture": id_info.get("picture", ""),
          "sub": id_info["sub"],
      }
    except ValueError as e:
      raise Exception(f"Invalid ID token: {e}")
