from fastapi import APIRouter
from app.config import get_settings

router = APIRouter(prefix="/api/admin/system", tags=["Admin System"])


@router.get("/config")
async def admin_system_config():
    """
    Returns non-sensitive runtime configuration.
    """
    settings = get_settings()
    return {
        "app_name": settings.APP_NAME,
        "env": settings.APP_ENV,
        "debug": settings.DEBUG,
        "log_level": settings.LOG_LEVEL,
    }
