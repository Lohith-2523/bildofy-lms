from sqlalchemy.ext.asyncio import AsyncSession
from app.models.notes import GeneratedNote
from app.schemas.notes import NotesGenerateRequest, NotesResponse
from app.ai import OllamaClient, select_model
from app.services.file_validation import validate_upload
from fastapi import UploadFile, HTTPException
import uuid
import os
from app.models.user import User
ollama = OllamaClient()

UPLOAD_DIR = "app/uploads/teacher_notes"
os.makedirs(UPLOAD_DIR, exist_ok=True)


async def create_manual_notes(
    payload: NotesGenerateRequest,
    db: AsyncSession,
) -> NotesResponse:
    """
    Teacher provides full content manually.
    """

    note = GeneratedNote(
        user_id=1,  # replaced by auth later
        subject=payload.subject,
        chapter=payload.chapter,
        difficulty=payload.difficulty,
        pdf_url="",
        extra_data={
            "mode": "manual",
            "content": payload.context.get("manual_content", ""),
        },
    )

    db.add(note)
    await db.commit()
    await db.refresh(note)

    return NotesResponse(
        content_id=str(note.id),
        summary="Manual notes created",
        pdf_url=None,
        offline_ready=False,
        expires_at=None,
    )


async def generate_teacher_notes(
    payload,
    db: AsyncSession,
    current_user: User,
):
    raw_content = payload.raw_ai_output

    if not raw_content or not raw_content.strip():
        raise HTTPException(status_code=400, detail="AI returned empty content")

    note = GeneratedNote(
        user_id=current_user.id,
        subject=payload.subject,
        chapter=payload.chapter,
        difficulty=payload.difficulty,
        content=raw_content,
        is_student_generated=False,
        is_teacher_provided=True,
    )

    db.add(note)
    await db.commit()
    await db.refresh(note)

    return note


async def upload_notes_file(
    subject: str,
    chapter: str,
    file: UploadFile,
    db: AsyncSession,
) -> NotesResponse:
    """
    Upload teacher-created PDF notes.
    """

    await validate_upload(file)

    ext = os.path.splitext(file.filename)[1]
    filename = f"{uuid.uuid4()}{ext}"
    path = os.path.join(UPLOAD_DIR, filename)

    with open(path, "wb") as f:
        f.write(await file.read())

    note = GeneratedNote(
        user_id=1,  # replaced by auth later
        subject=subject,
        chapter=chapter,
        difficulty="custom",
        pdf_url=path,
        is_student_generated=False,
        is_teacher_provided=True,
        extra_data={
            "mode": "upload",
            "original_filename": file.filename,
        },
    )

    db.add(note)
    await db.commit()
    await db.refresh(note)

    return NotesResponse(
        content_id=str(note.id),
        summary="Uploaded notes",
        pdf_url=path,
        offline_ready=True,
        expires_at=None,
    )
