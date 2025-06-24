
from pydantic import BaseModel, ConfigDict


class HealthBase(BaseModel):
    status: str
    message: str

    model_config = ConfigDict(from_attributes=True, extra="forbid")
