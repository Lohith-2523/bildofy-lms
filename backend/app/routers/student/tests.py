from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.routers.student._guards import student_guard

from app.db.session import get_db
from app.schemas.tests import TestCreateRequest, TestResponse
from app.services.test_service import generate_test
from app.services.xp_service import apply_xp_event

router = APIRouter(prefix="/api/student/tests", tags=["Student Tests"], dependencies=[student_guard])


@router.post("/generate", response_model=TestResponse)
async def generate_test_endpoint(
    payload: TestCreateRequest,
    db: AsyncSession = Depends(get_db),
):
    response = await generate_test(payload)
    await apply_xp_event(db, user_id=1, event="TEST_COMPLETED")
    return response
