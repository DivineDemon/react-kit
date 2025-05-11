from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from app.utils.crypto_util import decrypt_data, encrypt_data


class OTPBase(BaseModel):
  otp_code: str = Field(..., min_length=6, max_length=6)
  user_id: int
  expires_at: datetime


class OTPCreate(BaseModel):
  contact: str = Field(...,
                       description="Email or phone number to send the OTP")
  contact_type: str = Field(
      ..., description="Type of contact, e.g., email or phone")


class OTPVerify(BaseModel):
  otp_code: str = Field(...,
                        min_length=6,
                        max_length=6,
                        description="The OTP to verify")
  user_id: str


class OTPResponse(BaseModel):
  id: int
  otp_code: str
  user_id: str
  expires_at: datetime
  verified: bool

  @model_validator(mode="before")
  def encrypt_user_id(cls, values):
    if "user_id" in values:
      values["user_id"] = encrypt_data(values["user_id"])
    return values

  @model_validator(mode="after")
  def decrypt_user_id(cls, values):

    if "user_id" in values:
      values["user_id"] = decrypt_data(values["user_id"])
    return values

  @field_validator("expires_at", mode="before")
  def serialize_datetime(cls, value):
    if isinstance(value, datetime):
      return value.isoformat()
    return value

  class Config:
    from_attributes = True
