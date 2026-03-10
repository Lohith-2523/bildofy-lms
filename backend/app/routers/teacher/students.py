from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.security.dependencies import require_role, get_current_user
from app.models.user import UserRole
from app.services.teacher_context import get_teacher_subject
from app.services.teacher_student_service import get_students_for_subject

router = APIRouter(
    prefix="/teacher/students",
    tags=["Teacher"],
    dependencies=[Depends(require_role(UserRole.teacher))],
)


@router.get("")
async def list_students_for_teacher(
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    subject = await get_teacher_subject(current_user.id, db)
    students = await get_students_for_subject(subject, db)

    return [
        {
            "id": student.id,
            "name": student.name or f"Student {student.id}",
            "email": student.email,
            "class_id": student.class_id,
        }
        for student in students
    ]
