from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.routers.student._guards import student_guard

from app.db.session import get_db
from app.schemas.common import ClientContext
from app.services.ai_service import chat_with_ai
from app.services.xp_service import apply_xp_event

router = APIRouter(prefix="/api/student/ai", tags=["Student AI Chat"], dependencies=[student_guard])


@router.post("/chat")
async def ai_chat_endpoint(
    messages: list[dict],
    context: ClientContext,
    db: AsyncSession = Depends(get_db),
):
    response = await chat_with_ai(messages, context)
    await apply_xp_event(db, user_id=1, event="AI_CHAT_INTERACTION")
    return {"response": response}
