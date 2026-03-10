from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.routers.admin._guards import admin_guard
from app.schemas.admin_dashboard import (
    AssignTeacherSubjectRequest,
    CreateClassRequest,
    CreateTeacherRequest,
    InfrastructureConfigRequest,
    ReassignClassRequest,
)
from app.services.admin_dashboard_service import (
    admin_overview,
    assign_teacher_to_subject,
    bulk_import_students,
    create_class_with_subjects,
    create_teacher_user,
    get_infrastructure_config,
    list_classes,
    list_subjects,
    list_teachers,
    list_users,
    reassign_user_class,
    save_infrastructure_config,
    upload_licensed_content,
)

router = APIRouter(
    prefix="/api/admin/dashboard",
    tags=["Admin Dashboard"],
    dependencies=[admin_guard],
)


@router.get("/overview")
async def get_overview(db: AsyncSession = Depends(get_db)):
    return await admin_overview(db)


@router.get("/lookup/classes")
async def lookup_classes(db: AsyncSession = Depends(get_db)):
    return await list_classes(db)


@router.get("/lookup/subjects")
async def lookup_subjects(db: AsyncSession = Depends(get_db)):
    return await list_subjects(db)


@router.get("/lookup/teachers")
async def lookup_teachers(db: AsyncSession = Depends(get_db)):
    return await list_teachers(db)


@router.get("/lookup/users")
async def lookup_users(db: AsyncSession = Depends(get_db)):
    return await list_users(db)


@router.post("/teachers")
async def create_teacher(
    payload: CreateTeacherRequest,
    db: AsyncSession = Depends(get_db),
):
    return await create_teacher_user(payload, db)


@router.post("/classes")
async def create_class(
    payload: CreateClassRequest,
    db: AsyncSession = Depends(get_db),
):
    return await create_class_with_subjects(payload, db)


@router.post("/students/bulk-import")
async def import_students(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    return await bulk_import_students(file, db)


@router.get("/infrastructure")
async def read_infrastructure():
    return get_infrastructure_config()


@router.post("/infrastructure")
async def write_infrastructure(payload: InfrastructureConfigRequest):
    return save_infrastructure_config(payload)


@router.post("/licensed-content")
async def upload_school_licensed_content(
    school_id: str,
    board: str,
    grade: int,
    subject: str,
    chapter: str,
    file: UploadFile = File(...),
):
    return await upload_licensed_content(
        school_id=school_id,
        board=board,
        grade=grade,
        subject=subject,
        chapter=chapter,
        file=file,
    )


@router.post("/system/reassign-class")
async def system_reassign_class(
    payload: ReassignClassRequest,
    db: AsyncSession = Depends(get_db),
):
    return await reassign_user_class(payload, db)


@router.post("/system/assign-teacher-subject")
async def system_assign_teacher_subject(
    payload: AssignTeacherSubjectRequest,
    db: AsyncSession = Depends(get_db),
):
    return await assign_teacher_to_subject(payload, db)
