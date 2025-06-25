from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt

from app.core.config import settings


def create_access_token(data: dict[str, Any], expires_delta: int = 0):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + \
        timedelta(minutes=expires_delta or settings.JWT_EXPIRATION_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET,
                             algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET, algorithms=[
                             settings.JWT_ALGORITHM])
        return payload
    except JWTError:
        return None
