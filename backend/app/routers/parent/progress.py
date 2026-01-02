from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.services.parent_overview_service import get_detailed_progress

router = APIRouter(prefix="/api/parent/progress", tags=["Parent Progress"])


@router.get("/child/{student_id}")
async def parent_child_progress(
    student_id: int,
    db: AsyncSession = Depends(get_db),
):
    """
    Detailed progress breakdown for a parent.
    """
    return await get_detailed_progress(student_id, db)
