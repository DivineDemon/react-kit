from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.base import Base


class Item(Base): # ORM Model for Item
    __tablename__ = "items"

    image_url = Column(String, nullable=True)
    description = Column(String, nullable=False)
    name = Column(String, nullable=False, unique=True)
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="items")
