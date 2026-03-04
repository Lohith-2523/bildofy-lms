from starlette.middleware.base import BaseHTTPMiddleware
from app.db.session import AsyncSessionLocal
from app.models.audit_log import AuditLog


class AuditMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)

        user_id = getattr(request.state, "user_id", None)

        async with AsyncSessionLocal() as db:
            db.add(
                AuditLog(
                    user_id=user_id,
                    action=request.method,
                    endpoint=request.url.path,
                )
            )
            await db.commit()

        return response
