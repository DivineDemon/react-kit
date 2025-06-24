from fastapi import APIRouter

from app.routers.health_router import router as health_router
from app.routers.item_router import router as item_router

router = APIRouter()

router.include_router(health_router)
router.include_router(item_router, prefix="", tags=["items"])