from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

from app.models.subject import Subject
from app.models.subject_student import SubjectStudent
from app.services.enrollment_guard import validate_enrollment_allowed


async def enroll_student_in_subject(
    subject_id: int,
    student_id: int,
    db: AsyncSession,
):
    subject = await db.get(Subject, subject_id)
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")

    await validate_enrollment_allowed(subject, db)

    # Prevent duplicate enrollment
    result = await db.execute(
        select(SubjectStudent).where(
            SubjectStudent.subject_id == subject_id,
            SubjectStudent.student_id == student_id,
        )
    )
    if result.scalar():
        raise HTTPException(
            status_code=400,
            detail="Student already enrolled in subject",
        )

    enrollment = SubjectStudent(
        subject_id=subject_id,
        student_id=student_id,
    )

    db.add(enrollment)
    await db.commit()
