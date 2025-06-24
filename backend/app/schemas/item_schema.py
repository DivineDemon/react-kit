from typing import Optional

from pydantic import BaseModel, ConfigDict, HttpUrl


class ItemBase(BaseModel):
    name: str
    description: str
    image_url: HttpUrl

    model_config = ConfigDict(from_attributes=True, extra="forbid")


class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[HttpUrl] = None

    model_config = ConfigDict(from_attributes=True, extra="forbid")


class ItemRead(ItemBase):
    id: int
    name: str
    description: str
    image_url: HttpUrl

    model_config = ConfigDict(from_attributes=True, extra="forbid")


class ItemDelete(BaseModel):
    id: int

    model_config = ConfigDict(from_attributes=True, extra="forbid")
