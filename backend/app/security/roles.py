from app.models.user import UserRole as Role
from fastapi import Depends, HTTPException
from app.models.user import User
from app.security.dependencies import get_current_user


def require_role(*roles: str):
    async def role_guard(user: User = Depends(get_current_user)):
        if user.role not in roles:
            raise HTTPException(status_code=403, detail="Forbidden")
        return user
    return role_guard