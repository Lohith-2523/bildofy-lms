from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ...db.session import get_db
from ...repositories.assignment_repo import AssignmentRepo
from ...schemas.assignments import AssignmentOut
from app.routers.student._guards import student_guard

router = APIRouter(prefix="/api/student/assignments", tags=["student.assignments"], dependencies=[student_guard])
repo = AssignmentRepo()


@router.get("/", response_model=list[AssignmentOut])
async def list_assignments(db: AsyncSession = Depends(get_db)):
    rows = await repo.list(db)
    return rows
