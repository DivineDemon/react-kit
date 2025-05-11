from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text, func
from sqlalchemy.orm import relationship

from app.database.db_config import Base


class User(Base):
  __tablename__ = "users"

  id = Column(Integer, primary_key=True, index=True)
  username = Column(String(50), unique=True, nullable=False)
  email = Column(String(255), unique=True, nullable=False)
  phone_number = Column(String(15), unique=True, nullable=True)
  profile_picture_url = Column(Text, nullable=True)
  is_verified = Column(Boolean, default=False)
  created_at = Column(DateTime, default=func.now())
  updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

  auth = relationship("UserAuth",
                      back_populates="user",
                      cascade="all, delete-orphan")
  reset_tokens = relationship("ResetToken", back_populates="user")
