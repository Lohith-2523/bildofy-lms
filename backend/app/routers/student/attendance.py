from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.user import User
from app.routers.student._guards import student_guard
from app.security import get_current_user
from app.services.attendance_service import (
    student_attendance_records,
    student_attendance_summary,
)

router = APIRouter(
    prefix="/api/student/attendance",
    tags=["Student Attendance"],
    dependencies=[student_guard],
)


@router.get("/summary")
async def get_student_attendance_summary(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await student_attendance_summary(db=db, student_id=current_user.id)


@router.get("/")
async def get_student_attendance_records(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await student_attendance_records(db=db, student_id=current_user.id)
