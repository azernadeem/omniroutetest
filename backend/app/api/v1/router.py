from fastapi import APIRouter
from app.core.config import settings
from app.api.v1.market import router as market_router

router = APIRouter()

router.include_router(market_router)

@router.get("/health")
async def health():
    return {"status": "healthy", "service": "crypto-dashboard-backend"}

@router.get("/config")
async def get_config():
    return {
        "app_name": settings.APP_NAME,
        "api_v1_str": settings.API_V1_STR
    }