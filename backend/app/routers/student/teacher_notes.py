from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.models.notes import GeneratedNote
from app.routers.student._guards import student_guard
from fastapi.responses import FileResponse
from app.security import get_current_user
from app.models.user import User
from app.models.notes import GeneratedNote

router = APIRouter(
    prefix="/api/student/notes",
    tags=["Student Teacher Notes"],
    dependencies=[student_guard],
    redirect_slashes=False,
)


@router.get("/teacher")
async def list_teacher_notes(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(GeneratedNote).where(
            GeneratedNote.is_teacher_provided == True
        )
    )

    notes = result.scalars().all()

    return [
        {
            "id": n.id,
            "subject": n.subject,
            "chapter": n.chapter,
        }
        for n in notes
    ]



@router.get("/{note_id}")
async def get_teacher_note(note_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(GeneratedNote).where(
            GeneratedNote.id == note_id,
            GeneratedNote.is_teacher_provided == True,
        )
    )

    note = result.scalar_one_or_none()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    # PDF-based note
    if note.pdf_url:
        return {
            "type": "pdf",
            "url": note.pdf_url,
        }

    # AI / manual content
    return {
        "type": "markdown",
        "content": note.extra_data.get("content"),
    }


@router.get("/{note_id}/download")
async def download_teacher_note(note_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(GeneratedNote).where(
            GeneratedNote.id == note_id,
            GeneratedNote.is_teacher_provided == True,
        )
    )

    note = result.scalar_one_or_none()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    if note.pdf_url:
        return FileResponse(note.pdf_url)

    return {
        "content": note.extra_data.get("content"),
    }
