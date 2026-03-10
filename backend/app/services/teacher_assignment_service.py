import os
import uuid
from typing import Optional

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.assignments import Assignment
from app.models.user import User
from app.schemas.assignments import AssignmentResponse, TeacherAssignmentCreateRequest
from app.services.file_validation import validate_upload

LMS_PREFIX = "LMS::"
PDF_PREFIX = "PDF::"
UPLOAD_DIR = os.path.join("app", "uploads", "assignment_question_papers")


def _pack_description(mode: str, content: Optional[str]) -> str:
    if mode == "PDF":
        return f"{PDF_PREFIX}{content or ''}"
    return f"{LMS_PREFIX}{content or ''}"


def unpack_assignment_description(description: Optional[str]) -> tuple[str, str]:
    raw = description or ""
    if raw.startswith(PDF_PREFIX):
        return "PDF", raw[len(PDF_PREFIX):]
    if raw.startswith(LMS_PREFIX):
        return "LMS", raw[len(LMS_PREFIX):]
    return "LMS", raw


async def create_assignment(
    payload: TeacherAssignmentCreateRequest,
    db: AsyncSession,
    current_user: User,
) -> AssignmentResponse:
    assignment = Assignment(
        created_by=current_user.id,
        title=payload.title,
        subject=payload.subject,
        description=_pack_description(payload.mode, payload.content),
        due_date=payload.due_date,
    )

    db.add(assignment)
    await db.commit()
    await db.refresh(assignment)

    return AssignmentResponse(
        id=assignment.id,
        title=assignment.title,
        subject=assignment.subject,
        due_date=assignment.due_date,
    )


async def create_assignment_from_pdf(
    title: str,
    subject: str,
    due_date,
    file: UploadFile,
    db: AsyncSession,
    current_user: User,
) -> AssignmentResponse:
    await validate_upload(file)
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    filename = f"{uuid.uuid4().hex}_{file.filename}"
    path = os.path.join(UPLOAD_DIR, filename)

    content = await file.read()
    with open(path, "wb") as f:
        f.write(content)

    payload = TeacherAssignmentCreateRequest(
        title=title,
        subject=subject,
        due_date=due_date,
        mode="PDF",
        content=path,
    )

    return await create_assignment(payload, db, current_user)
