from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from fastapi import HTTPException


async def list_users(db: AsyncSession):
    result = await db.execute(select(User))
    return result.scalars().all()


async def get_user(user_id: int, db: AsyncSession):
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()
    if not user:
        return {"error": "User not found"}
    return user


async def update_user_role(
    user_id: int,
    role: str,
    db: AsyncSession,
):
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()
    if not user:
        return {"error": "User not found"}

    user.role = role
    await db.commit()
    await db.refresh(user)

    return {
        "user_id": user.id,
        "new_role": user.role,
    }


async def disable_user(
    user_id: int,
    db: AsyncSession,
):
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()
    if not user:
        return {"error": "User not found"}

    raise HTTPException(
        status_code=400,
        detail="User disable is not supported because 'is_active' is not present in schema",
    )
