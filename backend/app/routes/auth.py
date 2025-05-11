import os

from dotenv import load_dotenv
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.db_config import get_db
from app.schemas.auth import (
    ForgotPasswordRequest,
    LoginRequest,
    ResetPasswordRequest,
    SignUpRequest,
)
from app.services.auth_service import AuthService
from app.services.google_auth_service import GoogleAuthService

router = APIRouter(prefix="/auth", tags=["Auth"])

load_dotenv()

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"


@router.post("/signup")
def signup(data: SignUpRequest, db: Session = Depends(get_db)):
  auth_service = AuthService(db)
  return auth_service.signup(data)


@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
  auth_service = AuthService(db)
  return auth_service.login(
      username_or_email_or_phone=data.username_or_email_or_phone,
      password=data.password,
  )


@router.get("/google")
def google_login():
  return {"auth_url": GoogleAuthService.get_google_auth_url()}


@router.post("/login_or_signup_with_google")
def login_or_signup_with_google(code: str, db: Session = Depends(get_db)):
  """
    Log in or sign up with Google OAuth code.
    """
  auth_service = AuthService(db)
  return auth_service.login_or_signup_with_google(code, db)


@router.get("/google/callback")
def google_callback(code: str, db: Session = Depends(get_db)):
  """
    Handle the Google OAuth callback.
  """
  auth_service = AuthService(db)
  return auth_service.login_or_signup_with_google(code, db)


@router.post("/forgot-password")
def forgot_password(request: ForgotPasswordRequest,
                    db: Session = Depends(get_db)):
  auth_service = AuthService(db)
  return auth_service.forgot_password(email=request.email)


@router.post("/reset-password")
def reset_password(request: ResetPasswordRequest,
                   db: Session = Depends(get_db)):
  auth_service = AuthService(db)
  return auth_service.reset_password(
      token=request.token,
      new_password=request.new_password,
      confirm_password=request.confirm_password,
  )
