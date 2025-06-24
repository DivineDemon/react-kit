from fastapi import APIRouter

from app.schemas.generic import ResponseModel
from app.schemas.health_schema import HealthBase

router = APIRouter()


@router.get("/")
async def health_check() -> ResponseModel[HealthBase]:
    return ResponseModel(
        status=200,
        message="Health check successful",
        data=HealthBase(status="ok", message="Service is running")
    )
