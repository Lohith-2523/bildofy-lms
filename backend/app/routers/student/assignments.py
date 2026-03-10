import io
import os
import uuid

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import FileResponse, StreamingResponse
from fpdf import FPDF
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.assignments import Assignment
from app.models.user import User
from app.routers.student._guards import student_guard
from app.schemas.assignments import StudentAssignmentListItem
from app.security import get_current_user
from app.services.file_validation import validate_upload
from app.services.teacher_assignment_service import unpack_assignment_description

SUBMISSION_DIR = os.path.join("app", "uploads", "assignment_submissions")

router = APIRouter(
    prefix="/api/student/assignments",
    tags=["Student Assignments"],
    dependencies=[student_guard],
)


@router.get("/", response_model=list[StudentAssignmentListItem])
async def list_assignments(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Assignment).order_by(Assignment.created_at.desc())
    )
    assignments = result.scalars().all()

    items: list[StudentAssignmentListItem] = []
    for a in assignments:
        mode, _ = unpack_assignment_description(a.description)
        items.append(
            StudentAssignmentListItem(
                id=a.id,
                title=a.title,
                subject=a.subject,
                due_date=a.due_date,
                mode="PDF" if mode == "PDF" else "LMS",
            )
        )
    return items


@router.get("/{assignment_id}")
async def get_assignment(
    assignment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(Assignment).where(Assignment.id == assignment_id))
    assignment = result.scalar_one_or_none()
    if assignment is None:
        raise HTTPException(status_code=404, detail="Assignment not found")

    mode, content = unpack_assignment_description(assignment.description)
    return {
        "id": assignment.id,
        "title": assignment.title,
        "subject": assignment.subject,
        "due_date": assignment.due_date,
        "mode": mode,
        "content": content,
    }


@router.get("/{assignment_id}/paper/pdf")
async def export_assignment_paper_pdf(
    assignment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(Assignment).where(Assignment.id == assignment_id))
    assignment = result.scalar_one_or_none()
    if assignment is None:
        raise HTTPException(status_code=404, detail="Assignment not found")

    mode, content = unpack_assignment_description(assignment.description)
    if mode == "PDF":
        if not content or not os.path.exists(content):
            raise HTTPException(status_code=404, detail="Question paper PDF not found")
        return FileResponse(content, media_type="application/pdf")

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Helvetica", "B", 16)
    pdf.multi_cell(0, 10, txt=assignment.title or "Assignment")
    pdf.ln(2)
    pdf.set_font("Helvetica", "", 12)
    pdf.multi_cell(0, 8, txt=f"Subject: {assignment.subject}")
    pdf.multi_cell(0, 8, txt=f"Due Date: {assignment.due_date}")
    pdf.ln(4)
    pdf.multi_cell(0, 8, txt=content or "No assignment content provided.")

    output = bytes(pdf.output(dest="S"))
    return StreamingResponse(
        io.BytesIO(output),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="assignment_{assignment_id}_paper.pdf"'
        },
    )


@router.post("/{assignment_id}/submit")
async def submit_assignment_pdf(
    assignment_id: int,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(Assignment).where(Assignment.id == assignment_id))
    assignment = result.scalar_one_or_none()
    if assignment is None:
        raise HTTPException(status_code=404, detail="Assignment not found")

    await validate_upload(file)
    os.makedirs(SUBMISSION_DIR, exist_ok=True)

    filename = f"{assignment_id}_{current_user.id}_{uuid.uuid4().hex}.pdf"
    path = os.path.join(SUBMISSION_DIR, filename)

    data = await file.read()
    with open(path, "wb") as f:
        f.write(data)

    return {"ok": True, "assignment_id": assignment_id, "submission_path": path}
