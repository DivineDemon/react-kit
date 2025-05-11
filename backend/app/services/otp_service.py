from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.otp import OTP
from app.models.user import User
from app.utils.crypto_util import decrypt_data
from app.utils.email_util import send_email
from app.utils.otp_util import generate_otp, otp_expiry
from app.utils.sms_util import send_sms


class OTPService:

  def __init__(self, db: Session):
    self.db = db

  def generate_and_send_otp(self,
                            user_id: int,
                            contact: str,
                            contact_type: str = "email"):

    if not user_id or not isinstance(user_id, int):
      return {"error": "Invalid user_id"}
    if not contact or not isinstance(contact, str):
      return {"error": "Invalid contact information"}
    if contact_type not in ["email", "phone"]:
      return {"error": "Invalid contact type"}

    otp_code = generate_otp()
    expires_at = otp_expiry()

    try:
      otp_entry = OTP(user_id=user_id,
                      otp_code=otp_code,
                      expires_at=expires_at)
      self.db.add(otp_entry)
      self.db.commit()
    except Exception as e:
      self.db.rollback()
      return {"error": f"Database error: {str(e)}"}

    try:
      if contact_type == "email":
        send_email(
            to=contact,
            subject="Your OTP Code",
            body=f"Your OTP code is: {otp_code}. It will expire in 5 minutes.",
        )
      elif contact_type == "phone":
        send_sms(
            to=contact,
            message=
            f"Your OTP code is: {otp_code}. It will expire in 5 minutes.",
        )
    except Exception as e:
      self.db.rollback()
      return {"error": f"Failed to send OTP: {str(e)}"}

    return {"message": "OTP sent successfully", "expires_at": expires_at}

  ###

  def verify_otp(self, encrypted_user_id: str, otp_code: str):

    try:
      user_id = int(decrypt_data(encrypted_user_id))
    except Exception:
      raise HTTPException(status_code=400, detail="Invalid user ID")
    otp_entry = (self.db.query(OTP).filter(OTP.user_id == user_id,
                                           OTP.otp_code == otp_code).first())

    if not otp_entry:
      raise HTTPException(status_code=400, detail="Invalid OTP")

    if otp_entry.expires_at < datetime.utcnow():
      raise HTTPException(status_code=400, detail="OTP has expired")

    otp_entry.verified = True
    self.db.commit()

    user = self.db.query(User).filter(User.id == user_id).first()
    if user:
      user.is_verified = True
      self.db.commit()

    return {"message": "OTP verified successfully"}
