import uuid
from datetime import datetime, timedelta

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.reset_token import ResetToken
from app.models.user import User
from app.models.user_auth import UserAuth
from app.services.google_auth_service import GoogleAuthService
from app.services.otp_service import OTPService
from app.utils.crypto_util import encrypt_data
from app.utils.email_util import send_email
from app.utils.hashing import Hash
from app.utils.jwt import create_access_token


class AuthService:

  def __init__(self, db: Session):
    self.db = db

  def signup(self, data):
    if (self.db.query(User).filter(
        (User.email == data.email)
        | (User.username == data.username)
        | (User.phone_number == data.phone_number)).first()):
      raise HTTPException(status_code=400, detail="User already exists")

    if data.password != data.confirm_password:
      raise HTTPException(status_code=400, detail="Passwords do not match")

    if data.otp_type not in ["email", "phone", "both"]:
      raise HTTPException(status_code=400, detail="Invalid otp_type")

    if data.otp_type == "email" and not data.email:
      raise HTTPException(status_code=400,
                          detail="Email is required for email otp_type")
    elif data.otp_type == "phone" and not data.phone_number:
      raise HTTPException(status_code=400,
                          detail="Phone number is required for phone otp_type")

    hashed_password = Hash.hash(data.password)

    user = User(
        username=data.username,
        email=data.email,
        phone_number=data.phone_number if data.phone_number else None,
    )
    self.db.add(user)
    self.db.commit()
    self.db.refresh(user)

    user_auth = UserAuth(user_id=user.id,
                         auth_provider="password",
                         password_hash=hashed_password)
    self.db.add(user_auth)
    self.db.commit()

    otp_service = OTPService(self.db)
    contact_type = data.otp_type
    contact = None

    if contact_type == "email":
      contact = data.email
    elif contact_type == "phone":
      contact = data.phone_number

    otp_service.generate_and_send_otp(user_id=user.id,
                                      contact=contact,
                                      contact_type=contact_type)

    encrypted_user_id = encrypt_data(str(user.id))

    return {
        "message": "User registered successfully. OTP sent to verify account.",
        "user_id": encrypted_user_id,
    }

  def login(self, username_or_email_or_phone, password):
    user = (self.db.query(User).filter(
        (User.email == username_or_email_or_phone)
        | (User.username == username_or_email_or_phone)
        | (User.phone_number == username_or_email_or_phone)).first())

    if not user:
      raise HTTPException(status_code=400, detail="Invalid credentials")

    user_auth = (self.db.query(UserAuth).filter(
        UserAuth.user_id == user.id,
        UserAuth.auth_provider == "password").first())
    if not user_auth or not Hash.verify(password, user_auth.password_hash):
      raise HTTPException(status_code=400, detail="Invalid credentials")

    if not user.is_verified:
      otp_service = OTPService(self.db)
      contact = user.email if user.email else user.phone_number
      contact_type = "email" if user.email else "phone"

      otp_response = otp_service.generate_and_send_otp(
          user_id=user.id, contact=contact, contact_type=contact_type)
      encrypted_user_id = encrypt_data(str(user.id))

      return {
          "message":
          "Account not verified. An OTP has been sent to your registered contact.",
          "otp_sent_to": contact,
          "expires_at": otp_response["expires_at"],
          "user_id": encrypted_user_id,
      }

    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}

  def login_or_signup_with_google(self, code: str, db: Session):
    tokens = GoogleAuthService.exchange_code_for_tokens(code)

    user_info = GoogleAuthService.get_user_info(tokens["id_token"])
    email = user_info["email"]
    username = user_info.get("name", email.split("@")[0])

    user = db.query(User).filter(User.email == email).first()

    if not user:
      user = User(email=email, username=username, is_verified=True)
      db.add(user)
      db.commit()
      db.refresh(user)

      user_auth = UserAuth(
          user_id=user.id,
          auth_provider="google",
          password_hash=None,
      )
      db.add(user_auth)
      db.commit()

    access_token = create_access_token({"sub": str(user.id)})
    return {
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "username": user.username
        },
    }

  def forgot_password(self, email: str):
    user = self.db.query(User).filter(User.email == email).first()
    if not user:
      raise HTTPException(status_code=404, detail="User not found")

    reset_token = str(uuid.uuid4())
    expires_at = datetime.utcnow() + timedelta(minutes=15)

    new_reset_token = ResetToken(user_id=user.id,
                                 token=reset_token,
                                 expires_at=expires_at)
    self.db.add(new_reset_token)
    self.db.commit()

    reset_url = f"http://localhost:8000/auth/reset-password?token={reset_token}"
    email_content = f"""
        <p>Hello {user.username},</p>
        <p>Click the link below to reset your password:</p>
        <a href="{reset_url}">{reset_url}</a>
        <p>This link will expire in 15 minutes.</p>
        """
    send_email(to=user.email, subject="Password Reset", body=email_content)

    return {"message": "Password reset email sent"}

  def reset_password(self, token: str, new_password: str,
                     confirm_password: str):
    if new_password != confirm_password:
      raise HTTPException(status_code=400, detail="Passwords do not match")

    reset_token = (self.db.query(ResetToken).filter(
        ResetToken.token == token).first())
    if not reset_token or reset_token.expires_at < datetime.utcnow():
      raise HTTPException(status_code=400, detail="Invalid or expired token")

    user_auth = (self.db.query(UserAuth).filter(
        UserAuth.user_id == reset_token.user_id).first())
    if not user_auth:
      raise HTTPException(status_code=404,
                          detail="User authentication record not found")

    user_auth.password_hash = Hash.hash(new_password)
    self.db.add(user_auth)
    self.db.commit()

    self.db.delete(reset_token)
    self.db.commit()

    return {"message": "Password reset successfully"}
