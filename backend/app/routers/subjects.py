from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.subject import SubjectCreateRequest, SubjectResponse
from app.services.subject_service import create_subject
from app.security.dependencies import require_role
from app.models.user import UserRole

router = APIRouter(
    prefix="/subjects",
    tags=["Subjects"],
)


@router.post(
    "",
    response_model=SubjectResponse,
    dependencies=[Depends(require_role(UserRole.admin))]
)
async def create_subject_endpoint(
    payload: SubjectCreateRequest,
    db: AsyncSession = Depends(get_db),
):
    return await create_subject(payload, db)
