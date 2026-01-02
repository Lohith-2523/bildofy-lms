from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.services.teacher_report_service import get_student_report
from app.routers.teacher._guards import teacher_guard

router = APIRouter(prefix="/api/teacher/reports", tags=["Teacher Reports"])


@router.get("/student/{student_id}")
async def get_detailed_student_report(
    student_id: int,
    db: AsyncSession = Depends(get_db),
):
    """
    Returns a detailed academic + behavioral report for a student.
    """
    return await get_student_report(student_id, db)
