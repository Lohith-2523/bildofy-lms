from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.models.assignments import Assignment
from app.models.tests import Test

router = APIRouter(prefix="/api/admin/content", tags=["Admin Content"])


@router.get("/assignments")
async def admin_list_assignments(
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Assignment))
    return result.scalars().all()


@router.get("/tests")
async def admin_list_tests(
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Test))
    return result.scalars().all()
