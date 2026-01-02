from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.services.admin_user_service import (
    list_users,
    get_user,
    update_user_role,
    disable_user,
)

router = APIRouter(prefix="/api/admin/users", tags=["Admin Users"])


@router.get("/")
async def admin_list_users(
    db: AsyncSession = Depends(get_db),
):
    return await list_users(db)


@router.get("/{user_id}")
async def admin_get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await get_user(user_id, db)


@router.post("/{user_id}/role")
async def admin_update_user_role(
    user_id: int,
    role: str,
    db: AsyncSession = Depends(get_db),
):
    return await update_user_role(user_id, role, db)


@router.post("/{user_id}/disable")
async def admin_disable_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await disable_user(user_id, db)
