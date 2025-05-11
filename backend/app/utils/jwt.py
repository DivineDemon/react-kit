import os
from datetime import datetime, timedelta

from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

load_dotenv()

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30000

bearer_scheme = HTTPBearer()


def create_access_token(data: dict):
  """Create a JWT access token with an expiration."""
  to_encode = data.copy()
  expire = datetime.now(
      datetime.timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  to_encode.update({"exp": expire})
  return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_access_token(token: str):
  """Decode and verify a JWT token."""
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload
  except JWTError:
    raise HTTPException(status_code=401, detail="Invalid or expired token")


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme), ):
  """
    Extract and validate the user from the token.
    Expects the token in the 'Authorization' header as 'Bearer <token>'.
    """
  token = credentials.credentials
  try:
    payload = verify_access_token(token)
    user_id = payload.get("sub")
    if user_id is None:
      raise HTTPException(status_code=401,
                          detail="Invalid authentication credentials")
    return {"id": user_id}
  except JWTError:
    raise HTTPException(status_code=401,
                        detail="Invalid authentication credentials")
