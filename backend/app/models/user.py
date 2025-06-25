from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.core.base import Base


class User(Base): # ORM Model for User
  __tablename__ = "users"

  password = Column(String, nullable=False)
  last_name = Column(String, nullable=False)
  first_name = Column(String, nullable=False)
  profile_picture = Column(String, nullable=True)
  email = Column(String, nullable=False, unique=True)
  id = Column(Integer, primary_key=True, index=True, autoincrement=True)

  items = relationship("Item", back_populates="owner",
                       cascade="all, delete-orphan")
