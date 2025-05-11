import random
import string
from datetime import datetime, timedelta


def generate_otp(length=6) -> str:
  """Generate a numeric OTP of specified length."""
  return "".join(random.choices(string.digits, k=length))


def otp_expiry(minutes=5) -> datetime:
  """Return the expiry time for the OTP."""
  return datetime.utcnow() + timedelta(minutes=minutes)
