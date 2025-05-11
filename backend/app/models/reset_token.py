from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database.db_config import Base


class ResetToken(Base):
  __tablename__ = "reset_tokens"

  id = Column(Integer, primary_key=True, index=True)
  user_id = Column(Integer,
                   ForeignKey("users.id", ondelete="CASCADE"),
                   nullable=False)
  token = Column(String, nullable=False)
  expires_at = Column(DateTime, nullable=False)
  created_at = Column(DateTime, default=datetime.utcnow)

  user = relationship("User", back_populates="reset_tokens")
