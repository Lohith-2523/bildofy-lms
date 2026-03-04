from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.common import ClientContext
from app.services.flashcards_service import generate_flashcards
from app.services.xp_service import apply_xp_event
from app.routers.student._guards import student_guard

router = APIRouter(prefix="/api/student/flashcards", tags=["Student Flashcards"], dependencies=[student_guard])


@router.post("/generate")
async def generate_flashcards_endpoint(
    subject: str,
    chapter: str,
    context: ClientContext,
    db: AsyncSession = Depends(get_db),
):
    response = await generate_flashcards(subject, chapter, context)
    await apply_xp_event(db, user_id=1, event="FLASHCARDS_REVIEWED")
    return response
