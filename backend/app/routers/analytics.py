from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.security import get_current_user
from app.models.user import User, UserRole
from app.services.analytics_service import AnalyticsService
from app.services.analytics_student_service import StudentAnalyticsService

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/overview")
async def analytics_overview(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role == UserRole.teacher:
        return {
            "scope": "teacher",
            "teacher": {
                "id": current_user.id,
                "name": current_user.name or f"Teacher {current_user.id}",
            },
            "class": await AnalyticsService.class_overview(
                db=db, class_id=current_user.class_id
            ),
            "subjects": await AnalyticsService.subject_overview(
                db=db,
                teacher_id=current_user.id,
            ),
        }

    if current_user.role == UserRole.student:
        return {
            "scope": "student",
            "student": {
                "id": current_user.id,
                "name": current_user.name or f"Student {current_user.id}",
            },
            "data": await AnalyticsService.student_overview(
                db=db, student_id=current_user.id
            ),
        }

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Analytics not available for this role",
    )
@router.get("/students")
async def analytics_students(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != UserRole.teacher:
        raise HTTPException(status_code=403)

    return await StudentAnalyticsService.teacher_students_overview(
        db=db,
        teacher_id=current_user.id,
    )
