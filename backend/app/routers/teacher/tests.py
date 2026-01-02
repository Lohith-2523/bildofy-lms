from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Literal

from app.db.session import get_db
from app.schemas.tests import TestCreateRequest, TestResponse
from app.services.teacher_test_service import (
    create_test_manual,
    create_test_ai_assisted,
)
from app.routers.teacher._guards import teacher_guard

router = APIRouter(prefix="/api/teacher/tests", tags=["Teacher Tests"])


@router.post("/create", response_model=TestResponse)
async def create_test_endpoint(
    payload: TestCreateRequest,
    creation_mode: Literal["MANUAL", "AI_ASSISTED"],
    db: AsyncSession = Depends(get_db),
):
    """
    creation_mode:
    - MANUAL → teacher provides all questions
    - AI_ASSISTED → AI suggests questions & answers
    """
    if creation_mode == "AI_ASSISTED":
        return await create_test_ai_assisted(payload, db)

    return await create_test_manual(payload, db)
