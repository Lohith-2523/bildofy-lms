from sqlalchemy.ext.asyncio import AsyncSession
from app.models.notes import GeneratedNote
from app.schemas.notes import NotesGenerateRequest, NotesResponse
from app.ai import OllamaClient, select_model
from app.services.file_validation import validate_upload
from fastapi import UploadFile
import uuid
import os

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


async def create_ai_assisted_notes(
    payload: NotesGenerateRequest,
    db: AsyncSession,
) -> NotesResponse:
    """
    Teacher provides outline → AI expands.
    """

    model = select_model(payload.context)

    prompt = f"""
You are assisting a teacher.

Expand the following outline into
clear, syllabus-aligned notes.

Outline:
{payload.context.get("outline")}

Rules:
- Accurate
- Structured
- Teacher-reviewed
"""

    ai_content = await ollama.generate(
        prompt=prompt,
        model_name=model,
        temperature=0.25,
        max_tokens=1200,
    )

    note = GeneratedNote(
        user_id=1,
        subject=payload.subject,
        chapter=payload.chapter,
        difficulty=payload.difficulty,
        pdf_url="",
        extra_data={
            "mode": "ai_assisted",
            "content": ai_content,
        },
    )

    db.add(note)
    await db.commit()
    await db.refresh(note)

    return NotesResponse(
        content_id=str(note.id),
        summary=ai_content[:300],
        pdf_url=None,
        offline_ready=False,
        expires_at=None,
    )


async def upload_notes_file(
    subject: str,
    chapter: str,
    file: UploadFile,
    db: AsyncSession,
) -> NotesResponse:
    """
    Upload teacher-created PDF notes.
    """

    ext = os.path.splitext(file.filename)[1]
    filename = f"{uuid.uuid4()}{ext}"
    path = os.path.join(UPLOAD_DIR, filename)

    with open(path, "wb") as f:
        f.write(await file.read())

    note = GeneratedNote(
        user_id=1,
        subject=subject,
        chapter=chapter,
        difficulty="custom",
        pdf_url=path,
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
