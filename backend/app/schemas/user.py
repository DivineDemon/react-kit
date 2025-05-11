from typing import Optional

from pydantic import BaseModel, EmailStr, model_validator

from app.utils.crypto_util import decrypt_data, encrypt_data


class UserBase(BaseModel):
  username: str
  email: EmailStr
  phone_number: Optional[str] = None


class UserResponse(BaseModel):
  id: str
  username: str
  email: str
  phone_number: Optional[str]
  profile_picture_url: Optional[str]
  is_verified: bool

  @model_validator(mode="before")
  def encrypt_user_id(cls, values):
    if "id" in values:
      values["id"] = encrypt_data(values["id"])

    return values

  @model_validator(mode="after")
  def decrypt_user_id(cls, values):
    if "id" in values:
      values["id"] = decrypt_data(values["id"])
    return values
