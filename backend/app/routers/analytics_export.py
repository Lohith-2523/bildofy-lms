import csv
from io import StringIO
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.security import get_current_user
from app.models.user import User, UserRole
from app.services.analytics_student_service import StudentAnalyticsService

router = APIRouter(prefix="/analytics/export", tags=["Analytics Export"])


@router.get("/students.csv")
async def export_students_csv(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != UserRole.teacher:
        raise HTTPException(status_code=403)

    students = await StudentAnalyticsService.teacher_students_overview(
        db=db,
        teacher_id=current_user.id,
    )

    buffer = StringIO()
    writer = csv.DictWriter(
        buffer,
        fieldnames=students[0].keys() if students else []
    )
    writer.writeheader()
    writer.writerows(students)

    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=class_analytics.csv"},
    )
