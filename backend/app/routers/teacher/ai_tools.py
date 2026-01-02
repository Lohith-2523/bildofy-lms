from fastapi import APIRouter
from app.schemas.common import ClientContext
from app.services.teacher_ai_service import (
    suggest_test_questions,
    suggest_assignment_outline,
)
from app.routers.teacher._guards import teacher_guard

router = APIRouter(prefix="/api/teacher/ai", tags=["Teacher AI Tools"])


@router.post("/suggest/test")
async def ai_suggest_test_questions(
    subject: str,
    difficulty: str,
    context: ClientContext,
):
    return await suggest_test_questions(subject, difficulty, context)


@router.post("/suggest/assignment")
async def ai_suggest_assignment(
    subject: str,
    topic: str,
    context: ClientContext,
):
    return await suggest_assignment_outline(subject, topic, context)
