from fastapi import APIRouter

from app.routers.health_router import router as health_router
from app.routers.item_router import router as item_router
from app.routers.user_router import router as user_router

router = APIRouter()

router.include_router(health_router)
router.include_router(item_router, prefix="", tags=["items"])
router.include_router(user_router, prefix="", tags=["users"])