from datetime import datetime

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.user import User
from app.routers.teacher._guards import teacher_guard
from app.schemas.assignments import AssignmentResponse, TeacherAssignmentCreateRequest
from app.security import get_current_user
from app.services.teacher_assignment_service import (
    create_assignment,
    create_assignment_from_pdf,
)

router = APIRouter(
    prefix="/api/teacher/assignments",
    tags=["Teacher Assignments"],
    dependencies=[teacher_guard],
)


@router.post("/create", response_model=AssignmentResponse)
async def create_assignment_endpoint(
    payload: TeacherAssignmentCreateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await create_assignment(payload, db, current_user)


@router.post("/upload", response_model=AssignmentResponse)
async def upload_assignment_question_paper(
    title: str,
    subject: str,
    due_date: datetime,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await create_assignment_from_pdf(
        title=title,
        subject=subject,
        due_date=due_date,
        file=file,
        db=db,
        current_user=current_user,
    )
