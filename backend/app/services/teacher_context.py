from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

from app.models.subject import Subject
from app.models.user import User, UserRole


async def get_teacher_subject(
    teacher_id: int,
    db: AsyncSession,
) -> Subject:
    """
    Returns the subject taught by the teacher.
    Enforces exactly one subject per teacher (current system rule).
    """
    result = await db.execute(
        select(Subject).where(Subject.teacher_id == teacher_id)
    )
    subject = result.scalar_one_or_none()

    if not subject:
        raise HTTPException(
            status_code=403,
            detail="Teacher is not assigned to any subject",
        )

    return subject
