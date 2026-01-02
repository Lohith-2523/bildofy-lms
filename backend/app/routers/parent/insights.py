from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.services.parent_insights_service import get_parent_insights

router = APIRouter(prefix="/api/parent/insights", tags=["Parent Insights"])


@router.get("/child/{student_id}")
async def parent_ai_insights(
    student_id: int,
    db: AsyncSession = Depends(get_db),
):
    """
    AI-generated academic insights for parents.
    """
    return await get_parent_insights(student_id, db)
