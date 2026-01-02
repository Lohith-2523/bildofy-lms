from app.config import get_settings


async def get_system_status():
    settings = get_settings()

    return {
        "app": settings.APP_NAME,
        "environment": settings.APP_ENV,
        "debug": settings.DEBUG,
        "ollama_base": settings.OLLAMA_BASE_URL,
    }
