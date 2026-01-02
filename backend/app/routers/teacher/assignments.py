from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Literal

from app.db.session import get_db
from app.schemas.assignments import AssignmentCreateRequest, AssignmentResponse
from app.services.teacher_assignment_service import create_assignment
from app.routers.teacher._guards import teacher_guard

router = APIRouter(prefix="/api/teacher/assignments", tags=["Teacher Assignments"])


@router.post("/create", response_model=AssignmentResponse)
async def create_assignment_endpoint(
    payload: AssignmentCreateRequest,
    assignment_type: Literal["LMS_ATTEMPT", "PDF_UPLOAD"],
    db: AsyncSession = Depends(get_db),
):
    """
    assignment_type:
    - LMS_ATTEMPT → student answers inside LMS
    - PDF_UPLOAD → student uploads a PDF
    """
    return await create_assignment(payload, assignment_type, db)
