from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.user import User
from app.routers.teacher._guards import teacher_guard
from app.schemas.attendance import AttendanceMarkRequest
from app.security import get_current_user
from app.services.attendance_service import get_teacher_attendance_roster, mark_attendance

router = APIRouter(
    prefix="/api/teacher/attendance",
    tags=["Teacher Attendance"],
    dependencies=[teacher_guard],
)


@router.get("/roster")
async def get_attendance_roster(
    subject_id: int,
    attendance_date: date,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    rows = await get_teacher_attendance_roster(
        db=db,
        teacher_id=current_user.id,
        subject_id=subject_id,
        attendance_date=attendance_date,
    )
    return {"subject_id": subject_id, "attendance_date": attendance_date, "students": rows}


@router.post("/mark")
async def mark_attendance_for_day(
    payload: AttendanceMarkRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await mark_attendance(db=db, teacher_id=current_user.id, payload=payload)
