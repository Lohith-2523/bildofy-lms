from fastapi import HTTPException, status


def require_admin(role: str):
    """
    Enforces admin-only access.
    Replace role source with auth context later.
    """
    if role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required",
        )
