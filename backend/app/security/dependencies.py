from fastapi import Depends, HTTPException, status
from app.security.roles import Role


def get_current_user():
    """
    Temporary user context.
    Replace with JWT/session-based auth later.
    """
    return {
        "user_id": 1,
        "role": Role.ADMIN,  # change for testing
    }


def require_role(*allowed_roles: Role):
    def dependency(user=Depends(get_current_user)):
        if user["role"] not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )
        return user

    return dependency
