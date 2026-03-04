from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.security import get_current_user
from app.models.user import User, UserRole
from app.models.subject import Subject


router = APIRouter(prefix="/student/subjects", tags=["Student Subjects"])


@router.get("")
async def list_subjects_for_student(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != UserRole.student:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only students can view subjects",
        )

    result = await db.execute(select(Subject))
    subjects = result.scalars().all()

    return [{"id": s.id, "name": s.name} for s in subjects]
