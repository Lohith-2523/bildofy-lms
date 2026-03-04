from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.subject import SubjectType
from app.models.subject_student import SubjectStudent
from app.models.user import User, UserRole


async def get_students_for_subject(
    subject,
    db: AsyncSession,
):
    """
    Returns students visible to the teacher based on subject type.
    """

    # CORE SUBJECT → all students in the class
    if subject.type == SubjectType.core:
        result = await db.execute(
            select(User).where(
                User.role == UserRole.student,
                User.class_id == subject.class_id,
            )
        )
        return result.scalars().all()

    # ELECTIVE SUBJECT → only enrolled students
    result = await db.execute(
        select(User)
        .join(SubjectStudent, SubjectStudent.student_id == User.id)
        .where(SubjectStudent.subject_id == subject.id)
    )
    return result.scalars().all()
