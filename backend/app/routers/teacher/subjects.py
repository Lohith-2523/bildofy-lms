from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.subject import Subject
from app.models.user import User
from app.routers.teacher._guards import teacher_guard
from app.security import get_current_user

router = APIRouter(
    prefix="/api/teacher/subjects",
    tags=["Teacher Subjects"],
    dependencies=[teacher_guard],
)


@router.get("/")
async def list_teacher_subjects(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Subject).where(Subject.teacher_id == current_user.id).order_by(Subject.name)
    )
    subjects = result.scalars().all()
    return [
        {
            "id": s.id,
            "name": s.name,
            "type": s.type.value if hasattr(s.type, "value") else str(s.type),
            "class_id": s.class_id,
        }
        for s in subjects
    ]
