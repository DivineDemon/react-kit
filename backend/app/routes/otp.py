from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.db_config import get_db
from app.schemas.otp import OTPCreate, OTPVerify
from app.services.otp_service import OTPService

router = APIRouter(prefix="/otp", tags=["OTP"])


@router.post("/generate-manual")
def generate_manual_otp(user_id: int, db: Session = Depends(get_db)):
  """
    Manually generate an OTP for testing purposes.
    """
  otp_service = OTPService(db)
  contact = "example@test.com"
  contact_type = "email"
  return otp_service.generate_and_send_otp(user_id=user_id,
                                           contact=contact,
                                           contact_type=contact_type)


@router.post("/generate")
def generate_otp(data: OTPCreate, db: Session = Depends(get_db)):
  """
    Generate an OTP and send it to the user's contact.
    """
  otp_service = OTPService(db)
  return otp_service.generate_and_send_otp(user_id=data.user_id,
                                           contact=data.contact,
                                           contact_type=data.contact_type)


@router.post("/verify")
def verify_otp(data: OTPVerify, db: Session = Depends(get_db)):
  otp_service = OTPService(db)
  return otp_service.verify_otp(encrypted_user_id=data.user_id,
                                otp_code=data.otp_code)
