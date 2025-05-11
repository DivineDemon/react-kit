from fastapi import HTTPException
from pydantic import (
    BaseModel,
    EmailStr,
    field_validator,
    model_validator,
)

from app.utils.crypto_util import encrypt_data
from app.utils.email_validator import (
    validate_email_domain,
    validate_email_format,
    validate_email_mx_records,
)


class SignUpRequest(BaseModel):
  username: str
  email: str
  phone_number: str
  password: str
  confirm_password: str
  otp_type: str

  @model_validator(mode="before")
  def encrypt_user_id(cls, values):
    if "id" in values:
      values["id"] = encrypt_data(values["id"])

    return values

  @model_validator(mode="before")
  def validate_email(cls, values):
    email = values.get("email")
    if email:
      if not validate_email_format(email):
        raise HTTPException(status_code=400, detail="Invalid email format.")

      validate_email_domain(email)

      domain = email.split("@")[-1]
      validate_email_mx_records(domain)

    return values


class LoginRequest(BaseModel):
  username_or_email_or_phone: str
  password: str


class GoogleAuthCallback(BaseModel):
  code: str


class ForgotPasswordRequest(BaseModel):
  email: EmailStr

  @field_validator("email")
  def validate_email(cls, value: str):
    if not validate_email_format(value):
      raise HTTPException(status_code=400, detail="Invalid email format.")
    validate_email_domain(value)
    domain = value.split("@")[-1]
    validate_email_mx_records(domain)
    return value


class ResetPasswordRequest(BaseModel):
  token: str
  new_password: str
  confirm_password: str
