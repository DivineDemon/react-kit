from sqlalchemy import Column, Integer, String

from app.core.base import Base


class Item(Base):  # ORM Model for Item
    __tablename__ = "items"

    image_url = Column(String, nullable=True)
    description = Column(String, nullable=False)
    name = Column(String, nullable=False, unique=True)
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
