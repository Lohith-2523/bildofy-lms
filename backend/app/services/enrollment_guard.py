from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.models.subject import Subject, SubjectType
from app.models.subject_student import SubjectStudent


async def validate_enrollment_allowed(
    subject: Subject,
    db: AsyncSession,
):
    """
    Validates whether enrollment is allowed for a subject.
    Does NOT perform enrollment.
    """

    # Core subjects cannot be manually enrolled
    if subject.type == SubjectType.core:
        raise HTTPException(
            status_code=400,
            detail="Enrollment not allowed for core subjects",
        )

    now = datetime.utcnow()

    # Enrollment window validation
    if subject.enrollment_open_at and now < subject.enrollment_open_at:
        raise HTTPException(
            status_code=403,
            detail="Enrollment window has not opened yet",
        )

    if subject.enrollment_close_at and now > subject.enrollment_close_at:
        raise HTTPException(
            status_code=403,
            detail="Enrollment window has closed",
        )

    # Capacity validation
    if subject.max_students is not None:
        result = await db.execute(
            select(func.count())
            .select_from(SubjectStudent)
            .where(SubjectStudent.subject_id == subject.id)
        )
        enrolled_count = result.scalar()

        if enrolled_count >= subject.max_students:
            raise HTTPException(
                status_code=409,
                detail="Subject enrollment is full",
            )
