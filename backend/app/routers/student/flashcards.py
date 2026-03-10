from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.schemas.flashcards import FlashcardsGenerateRequest
from app.services.flashcards_service import generate_flashcards
from app.services.xp_service import apply_xp_event
from app.routers.student._guards import student_guard
from app.security import get_current_user
from app.models.user import User
from app.models.flashcards import FlashcardSet

router = APIRouter(prefix="/api/student/flashcards", tags=["Student Flashcards"], dependencies=[student_guard])


@router.post("/generate")
async def generate_flashcards_endpoint(
    payload: FlashcardsGenerateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    generated = await generate_flashcards(payload.subject, payload.chapter, payload.context)

    flashcard_set = FlashcardSet(
        user_id=current_user.id,
        subject=payload.subject,
        chapter=payload.chapter,
        cards=[card.model_dump() for card in generated.cards],
    )

    db.add(flashcard_set)
    await db.commit()
    await db.refresh(flashcard_set)

    await apply_xp_event(db, user_id=current_user.id, event="FLASHCARDS_REVIEWED")

    return {
        "set_id": flashcard_set.id,
        "subject": flashcard_set.subject,
        "chapter": flashcard_set.chapter,
        "cards": flashcard_set.cards,
    }


@router.get("/")
async def list_flashcard_sets(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(FlashcardSet)
        .where(FlashcardSet.user_id == current_user.id)
        .order_by(FlashcardSet.created_at.desc())
    )
    sets = result.scalars().all()

    return [
        {
            "id": s.id,
            "subject": s.subject,
            "chapter": s.chapter,
            "cards_count": len(s.cards or []),
            "created_at": s.created_at,
        }
        for s in sets
    ]


@router.get("/{set_id}")
async def get_flashcard_set(
    set_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(FlashcardSet).where(
            FlashcardSet.id == set_id,
            FlashcardSet.user_id == current_user.id,
        )
    )
    set_row = result.scalar_one_or_none()

    if set_row is None:
        raise HTTPException(status_code=404, detail="Flashcard set not found")

    return {
        "set_id": set_row.id,
        "subject": set_row.subject,
        "chapter": set_row.chapter,
        "cards": set_row.cards,
        "created_at": set_row.created_at,
    }


@router.delete("/{set_id}")
async def delete_flashcard_set(
    set_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(FlashcardSet).where(
            FlashcardSet.id == set_id,
            FlashcardSet.user_id == current_user.id,
        )
    )
    set_row = result.scalar_one_or_none()

    if set_row is None:
        raise HTTPException(status_code=404, detail="Flashcard set not found")

    await db.delete(set_row)
    await db.commit()

    return {"ok": True, "deleted_set_id": set_id}
