from typing import Optional

from pydantic import BaseModel, ConfigDict, HttpUrl


class UserBase(BaseModel):
  email: str
  password: str
  last_name: str
  first_name: str
  profile_picture: Optional[HttpUrl] = None

  model_config = ConfigDict(from_attributes=True, extra="forbid")

class UserLogin(BaseModel):
  email: str
  password: str

  model_config = ConfigDict(from_attributes=True, extra="forbid")

class UserRead(UserBase):
  id: int
  email: str
  password: str
  last_name: str
  first_name: str
  token: Optional[str] = None
  profile_picture: Optional[HttpUrl] = None

  model_config = ConfigDict(from_attributes=True, extra="forbid")

class UserUpdate(BaseModel):
  email: Optional[str] = None
  last_name: Optional[str] = None
  first_name: Optional[str] = None
  new_password: Optional[str] = None
  current_password: Optional[str] = None
  profile_picture: Optional[HttpUrl] = None

  model_config = ConfigDict(from_attributes=True, extra="forbid")

class UserDelete(BaseModel):
  id: int

  model_config = ConfigDict(from_attributes=True, extra="forbid")

class UserJWT(BaseModel):
  sub: str
  user_id: int

  model_config = ConfigDict(from_attributes=True, extra="forbid")