from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.services.parent_overview_service import get_parent_overview

router = APIRouter(prefix="/api/parent/overview", tags=["Parent Overview"])


@router.get("/child/{student_id}")
async def parent_child_overview(
    student_id: int,
    db: AsyncSession = Depends(get_db),
):
    """
    High-level academic overview for a parent.
    """
    return await get_parent_overview(student_id, db)
