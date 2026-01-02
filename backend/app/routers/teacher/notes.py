from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Literal

from app.db.session import get_db
from app.routers.teacher._guards import teacher_guard
from app.schemas.notes import NotesGenerateRequest, NotesResponse
from app.services.teacher_notes_service import (
    create_manual_notes,
    create_ai_assisted_notes,
    upload_notes_file,
)

router = APIRouter(
    prefix="/api/teacher/notes",
    tags=["Teacher Notes"],
    dependencies=[teacher_guard],
)


@router.post("/create")
async def create_notes(
    payload: NotesGenerateRequest,
    creation_mode: Literal["MANUAL", "AI_ASSISTED"],
    db: AsyncSession = Depends(get_db),
):
    """
    MANUAL → teacher writes content fully
    AI_ASSISTED → teacher provides outline, AI expands
    """
    if creation_mode == "AI_ASSISTED":
        return await create_ai_assisted_notes(payload, db)

    return await create_manual_notes(payload, db)


@router.post("/upload")
async def upload_notes(
    subject: str,
    chapter: str,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    """
    Upload teacher-created notes (PDF).
    """
    return await upload_notes_file(subject, chapter, file, db)
