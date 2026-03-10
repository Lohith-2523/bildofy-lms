from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Literal

from app.db.session import get_db
from app.models.user import User
from app.routers.teacher._guards import teacher_guard
from app.schemas.tests import (
    TeacherAISuggestQuestionRequest,
    TeacherAISuggestQuestionResponse,
    TeacherManualTestCreateRequest,
    TestCreateRequest,
    TestResponse,
)
from app.security import get_current_user
from app.services.teacher_test_service import (
    create_test_ai_assisted,
    create_test_manual,
    suggest_single_question,
)

router = APIRouter(
    prefix="/api/teacher/tests",
    tags=["Teacher Tests"],
    dependencies=[teacher_guard],
)


@router.post("/create", response_model=TestResponse)
async def create_test_endpoint(
    payload: TestCreateRequest,
    creation_mode: Literal["MANUAL", "AI_ASSISTED"],
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if creation_mode == "AI_ASSISTED":
        test = await create_test_ai_assisted(payload, db, current_user)
        return TestResponse(
            test_id=test.id,
            title=test.title,
            total_marks=test.total_questions,
        )
    raise HTTPException(
        status_code=400,
        detail="Use /api/teacher/tests/create-manual for manual question creation",
    )


@router.post("/create-manual", response_model=TestResponse)
async def create_test_manual_endpoint(
    payload: TeacherManualTestCreateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await create_test_manual(payload, db, current_user)


@router.post("/ai-suggest-question", response_model=TeacherAISuggestQuestionResponse)
async def ai_suggest_single_question(
    payload: TeacherAISuggestQuestionRequest,
):
    return await suggest_single_question(
        subject=payload.subject,
        chapter=payload.chapter,
        difficulty=payload.difficulty,
        question_type=payload.question_type,
    )
