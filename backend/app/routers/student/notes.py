from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.schemas.notes import NotesGenerateRequest, NotesResponse
from app.services.notes_service import generate_student_notes
from app.services.xp_service import apply_xp_event
from app.routers.student._guards import student_guard
from app.security import get_current_user
from app.models.user import User
from app.models.notes import GeneratedNote

router = APIRouter(prefix="/api/student/notes", tags=["Student Notes"], dependencies=[student_guard])


@router.post("/generate")
async def generate_notes_endpoint(
    payload: NotesGenerateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    response = await generate_student_notes(payload, db, current_user)
    await apply_xp_event(
        db=db,
        user_id=current_user.id,
        event="NOTES_GENERATED"
    )

    return response

@router.get("/")
async def list_student_notes(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(GeneratedNote).where(
            GeneratedNote.user_id == current_user.id,
            GeneratedNote.is_student_generated == True,
        )
    )

    notes = result.scalars().all()

    return [
        {
            "id": n.id,
            "subject": n.subject,
            "chapter": n.chapter,
            "difficulty": n.difficulty,
            "created_at": n.created_at,
        }
        for n in notes
    ]
