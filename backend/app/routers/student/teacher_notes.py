from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.routers.student._guards import student_guard
from app.models.notes import GeneratedNote

router = APIRouter(
    prefix="/api/student/notes/teacher",
    tags=["Student Teacher Notes"],
    dependencies=[student_guard],
)


@router.get("/")
async def list_teacher_notes(
    db: AsyncSession = Depends(get_db),
):
    """
    List all teacher-created notes available to students.
    """
    result = await db.execute(
        select(GeneratedNote)
    )
    notes = result.scalars().all()

    return [
        {
            "id": n.id,
            "subject": n.subject,
            "chapter": n.chapter,
            "difficulty": n.difficulty,
            "mode": n.extra_data.get("mode") if n.extra_data else None,
            "pdf_url": n.pdf_url,
        }
        for n in notes
    ]


@router.get("/{note_id}")
async def get_teacher_note(
    note_id: int,
    db: AsyncSession = Depends(get_db),
):
    """
    Fetch a specific teacher note.
    """
    result = await db.execute(
        select(GeneratedNote).where(GeneratedNote.id == note_id)
    )
    note = result.scalar_one_or_none()

    if not note:
        return {"error": "Note not found"}

    return {
        "id": note.id,
        "subject": note.subject,
        "chapter": note.chapter,
        "difficulty": note.difficulty,
        "content": note.extra_data.get("content") if note.extra_data else None,
        "pdf_url": note.pdf_url,
    }
