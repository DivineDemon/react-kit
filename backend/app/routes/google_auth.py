from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.db_config import get_db
from app.services.auth_service import AuthService

router = APIRouter()


@router.get("/google/callback")
def google_callback(code: str, db: Session = Depends(get_db)):
  """
    Google login callback handler.
    This route will receive the code from Google OAuth and authenticate the user.
    """
  auth_service = AuthService(db)
  return auth_service.login_or_signup_with_google(code)
