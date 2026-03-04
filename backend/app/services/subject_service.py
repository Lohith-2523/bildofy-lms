from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

from app.models.subject import Subject, SubjectType
from app.models.subject_student import SubjectStudent
from app.models.user import User, UserRole
from app.schemas.subject import SubjectCreateRequest


async def create_subject(payload: SubjectCreateRequest, db: AsyncSession):
    # Core subjects MUST have class_id
    if payload.type == SubjectType.core and payload.class_id is None:
        raise HTTPException(
            status_code=400,
            detail="Core subjects must be linked to a class",
        )

    subject = Subject(
        name=payload.name,
        type=payload.type,
        class_id=payload.class_id,
        teacher_id=payload.teacher_id,
    )

    db.add(subject)
    await db.flush()

    # AUTO-ENROLL students for CORE subjects
    if payload.type == SubjectType.core:
        result = await db.execute(
            select(User).where(
                User.role == UserRole.student,
                User.class_id == payload.class_id,
            )
        )
        students = result.scalars().all()

        for student in students:
            enrollment = SubjectStudent(
                subject_id=subject.id,
                student_id=student.id,
            )
            db.add(enrollment)

    await db.commit()
    await db.refresh(subject)

    return subject
