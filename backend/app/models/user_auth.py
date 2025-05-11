from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import relationship

from app.database.db_config import Base


class UserAuth(Base):
  __tablename__ = "user_auth"

  id = Column(Integer, primary_key=True, index=True)
  user_id = Column(Integer,
                   ForeignKey("users.id", ondelete="CASCADE"),
                   nullable=False)
  auth_provider = Column(String(50), nullable=False)
  password_hash = Column(Text, nullable=True)
  oauth_provider_id = Column(String(255), nullable=True)
  oauth_access_token = Column(Text, nullable=True)
  created_at = Column(DateTime, default=func.now())
  updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

  user = relationship("User", back_populates="auth")
