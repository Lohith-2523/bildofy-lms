from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, case

from app.models.progress import Progress
from app.models.assignments import Assignment
from app.models.test import Test
from app.models.attendance import AttendanceRecord


async def get_parent_overview(
    student_id: int,
    db: AsyncSession,
) -> dict:
    """
    High-level snapshot for parents.
    """

    progress_result = await db.execute(
        select(Progress).where(Progress.user_id == student_id)
    )
    progress = progress_result.scalar_one_or_none()

    assignments_result = await db.execute(
        select(Assignment).where(Assignment.created_by == student_id)
    )
    assignments = assignments_result.scalars().all()

    tests_result = await db.execute(
        select(Test).where(Test.created_by == student_id)
    )
    tests = tests_result.scalars().all()

    attendance_result = await db.execute(
        select(
            func.count(AttendanceRecord.id).label("total"),
            func.sum(case((AttendanceRecord.present == True, 1), else_=0)).label("present"),
        ).where(AttendanceRecord.student_id == student_id)
    )
    attendance = attendance_result.one()
    attendance_total = int(attendance.total or 0)
    attendance_present = int(attendance.present or 0)

    return {
        "student_id": student_id,
        "xp": progress.xp if progress else 0,
        "level": progress.level if progress else 1,
        "assignments_assigned": len(assignments),
        "tests_attempted": len(tests),
        "attendance_percentage": round((attendance_present / attendance_total) * 100, 2)
        if attendance_total
        else 0.0,
    }


async def get_detailed_progress(
    student_id: int,
    db: AsyncSession,
) -> dict:
    """
    Detailed academic breakdown.
    """

    progress_result = await db.execute(
        select(Progress).where(Progress.user_id == student_id)
    )
    progress = progress_result.scalar_one_or_none()

    attendance_result = await db.execute(
        select(
            func.count(AttendanceRecord.id).label("total"),
            func.sum(case((AttendanceRecord.present == True, 1), else_=0)).label("present"),
        ).where(AttendanceRecord.student_id == student_id)
    )
    attendance = attendance_result.one()
    attendance_total = int(attendance.total or 0)
    attendance_present = int(attendance.present or 0)

    return {
        "student_id": student_id,
        "xp": progress.xp if progress else 0,
        "level": progress.level if progress else 1,
        "stats": progress.stats if progress else {},
        "attendance_percentage": round((attendance_present / attendance_total) * 100, 2)
        if attendance_total
        else 0.0,
    }
