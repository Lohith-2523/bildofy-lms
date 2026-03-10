import csv
import io
import json
import os
import uuid
from datetime import datetime
from typing import Any

import pandas as pd
from PyPDF2 import PdfReader
from fastapi import HTTPException, UploadFile
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.classroom import Classroom
from app.models.subject import Subject, SubjectType
from app.models.user import User, UserRole
from app.schemas.admin_dashboard import (
    AssignTeacherSubjectRequest,
    CreateClassRequest,
    CreateTeacherRequest,
    InfrastructureConfigRequest,
    ReassignClassRequest,
)
from app.security.passwords import hash_password
from app.services.file_validation import validate_upload

ADMIN_DATA_DIR = os.path.join("app", "uploads", "admin")
INFRA_FILE = os.path.join(ADMIN_DATA_DIR, "infrastructure.json")
LICENSED_DIR = os.path.join(ADMIN_DATA_DIR, "licensed_content")


def _ensure_admin_dirs() -> None:
    os.makedirs(ADMIN_DATA_DIR, exist_ok=True)
    os.makedirs(LICENSED_DIR, exist_ok=True)


def _load_infra() -> dict[str, Any]:
    _ensure_admin_dirs()
    if not os.path.exists(INFRA_FILE):
        return {
            "boards": ["CBSE", "ICSE", "State"],
            "grades": [9, 10, 11, 12],
            "subject_mapping": {},
            "chapter_metadata": {},
            "licensed_content": [],
        }
    with open(INFRA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_infra(data: dict[str, Any]) -> None:
    _ensure_admin_dirs()
    with open(INFRA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


async def create_teacher_user(payload: CreateTeacherRequest, db: AsyncSession):
    existing = await db.execute(select(User).where(User.email == payload.email))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Teacher email already exists")

    teacher = User(
        name=payload.name,
        email=payload.email,
        password_hash=hash_password(payload.password),
        role=UserRole.teacher,
        class_id=payload.class_id,
    )
    db.add(teacher)
    await db.flush()

    if payload.subject_ids:
        result = await db.execute(
            select(Subject).where(Subject.id.in_(payload.subject_ids))
        )
        subjects = result.scalars().all()
        for subject in subjects:
            subject.teacher_id = teacher.id

    await db.commit()
    await db.refresh(teacher)
    return {
        "id": teacher.id,
        "name": teacher.name,
        "email": teacher.email,
        "class_id": teacher.class_id,
    }


async def create_class_with_subjects(payload: CreateClassRequest, db: AsyncSession):
    existing = await db.execute(
        select(Classroom).where(Classroom.code_prefix == payload.code_prefix)
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Class code_prefix already exists")

    classroom = Classroom(
        grade=payload.grade,
        section=payload.section,
        code_prefix=payload.code_prefix,
    )
    db.add(classroom)
    await db.flush()

    created_subjects = []
    for s in payload.subjects:
        subject = Subject(
            name=s.name,
            type=SubjectType.core if s.type == "core" else SubjectType.extracurricular,
            class_id=classroom.id if s.type == "core" else None,
            teacher_id=s.teacher_id,
        )
        db.add(subject)
        await db.flush()
        created_subjects.append({"id": subject.id, "name": subject.name, "type": s.type})

    await db.commit()
    await db.refresh(classroom)

    return {
        "class": {
            "id": classroom.id,
            "grade": classroom.grade,
            "section": classroom.section,
            "code_prefix": classroom.code_prefix,
        },
        "subjects": created_subjects,
    }


def _parse_student_rows_from_pdf(data: bytes) -> list[dict[str, str]]:
    reader = PdfReader(io.BytesIO(data))
    text = "\n".join([page.extract_text() or "" for page in reader.pages])
    rows: list[dict[str, str]] = []
    for line in text.splitlines():
        line = line.strip()
        if not line or "@" not in line:
            continue
        parts = [p.strip() for p in line.split(",")]
        if len(parts) < 4:
            continue
        rows.append(
            {
                "name": parts[0],
                "email": parts[1],
                "password": parts[2],
                "class_id": parts[3],
            }
        )
    return rows


async def bulk_import_students(file: UploadFile, db: AsyncSession):
    filename = (file.filename or "").lower()
    content = await file.read()

    rows: list[dict[str, Any]] = []
    if filename.endswith(".xlsx") or filename.endswith(".xls"):
        df = pd.read_excel(io.BytesIO(content))
        rows = df.to_dict(orient="records")
    elif filename.endswith(".csv"):
        decoded = content.decode("utf-8")
        rows = list(csv.DictReader(io.StringIO(decoded)))
    elif filename.endswith(".pdf"):
        rows = _parse_student_rows_from_pdf(content)
    else:
        raise HTTPException(status_code=400, detail="Supported formats: Excel, CSV, PDF")

    created = 0
    skipped = 0
    errors: list[str] = []

    for row in rows:
        try:
            email = str(row.get("email", "")).strip()
            if not email:
                skipped += 1
                continue

            existing = await db.execute(select(User).where(User.email == email))
            if existing.scalar_one_or_none():
                skipped += 1
                continue

            class_id_raw = row.get("class_id")
            class_id = int(class_id_raw) if class_id_raw not in (None, "") else None

            user = User(
                name=str(row.get("name", "")).strip() or None,
                email=email,
                password_hash=hash_password(str(row.get("password", "Temp@12345"))),
                role=UserRole.student,
                class_id=class_id,
            )
            db.add(user)
            created += 1
        except Exception as exc:
            skipped += 1
            errors.append(str(exc))

    await db.commit()
    return {"created": created, "skipped": skipped, "errors": errors[:20]}


def get_infrastructure_config():
    return _load_infra()


def save_infrastructure_config(payload: InfrastructureConfigRequest):
    current = _load_infra()
    current["boards"] = payload.boards
    current["grades"] = payload.grades
    current["subject_mapping"] = payload.subject_mapping
    current["chapter_metadata"] = payload.chapter_metadata
    _save_infra(current)
    return current


async def upload_licensed_content(
    school_id: str,
    board: str,
    grade: int,
    subject: str,
    chapter: str,
    file: UploadFile,
):
    await validate_upload(file)
    _ensure_admin_dirs()

    school_dir = os.path.join(LICENSED_DIR, school_id)
    os.makedirs(school_dir, exist_ok=True)
    saved_name = f"{uuid.uuid4().hex}_{file.filename}"
    path = os.path.join(school_dir, saved_name)

    with open(path, "wb") as f:
        f.write(await file.read())

    infra = _load_infra()
    infra.setdefault("licensed_content", []).append(
        {
            "id": uuid.uuid4().hex,
            "school_id": school_id,
            "board": board,
            "grade": grade,
            "subject": subject,
            "chapter": chapter,
            "path": path,
            "uploaded_at": datetime.utcnow().isoformat(),
        }
    )
    _save_infra(infra)
    return {"ok": True, "school_id": school_id, "path": path}


async def reassign_user_class(payload: ReassignClassRequest, db: AsyncSession):
    result = await db.execute(select(User).where(User.id == payload.user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.class_id = payload.class_id
    await db.commit()
    await db.refresh(user)
    return {"user_id": user.id, "class_id": user.class_id}


async def assign_teacher_to_subject(payload: AssignTeacherSubjectRequest, db: AsyncSession):
    teacher_result = await db.execute(
        select(User).where(User.id == payload.teacher_id, User.role == UserRole.teacher)
    )
    teacher = teacher_result.scalar_one_or_none()
    if not teacher:
        raise HTTPException(status_code=400, detail="Teacher not found")

    subject_result = await db.execute(select(Subject).where(Subject.id == payload.subject_id))
    subject = subject_result.scalar_one_or_none()
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")

    subject.teacher_id = payload.teacher_id
    await db.commit()
    await db.refresh(subject)
    return {"subject_id": subject.id, "teacher_id": subject.teacher_id}


async def admin_overview(db: AsyncSession):
    teachers = await db.scalar(select(func.count()).select_from(User).where(User.role == UserRole.teacher))
    students = await db.scalar(select(func.count()).select_from(User).where(User.role == UserRole.student))
    classes = await db.scalar(select(func.count()).select_from(Classroom))
    subjects = await db.scalar(select(func.count()).select_from(Subject))
    return {
        "teachers": teachers or 0,
        "students": students or 0,
        "classes": classes or 0,
        "subjects": subjects or 0,
    }


async def list_classes(db: AsyncSession):
    result = await db.execute(select(Classroom).order_by(Classroom.grade, Classroom.section))
    classes = result.scalars().all()
    return [
        {
            "id": c.id,
            "label": f"Grade {c.grade}-{c.section} (#{c.id})",
            "grade": c.grade,
            "section": c.section,
        }
        for c in classes
    ]


async def list_subjects(db: AsyncSession):
    result = await db.execute(select(Subject).order_by(Subject.name))
    subjects = result.scalars().all()
    return [
        {
            "id": s.id,
            "label": f"{s.name} (#{s.id})",
            "name": s.name,
            "type": s.type.value if hasattr(s.type, "value") else str(s.type),
            "teacher_id": s.teacher_id,
            "class_id": s.class_id,
        }
        for s in subjects
    ]


async def list_teachers(db: AsyncSession):
    result = await db.execute(
        select(User).where(User.role == UserRole.teacher).order_by(User.name, User.email)
    )
    teachers = result.scalars().all()
    return [
        {
            "id": t.id,
            "label": f"{(t.name or t.email)} (#{t.id})",
            "name": t.name,
            "email": t.email,
        }
        for t in teachers
    ]


async def list_users(db: AsyncSession):
    result = await db.execute(select(User).order_by(User.id))
    users = result.scalars().all()
    return [
        {
            "id": u.id,
            "label": f"{(u.name or u.email)} [{u.role}] (#{u.id})",
            "role": u.role.value if hasattr(u.role, "value") else str(u.role),
            "class_id": u.class_id,
        }
        for u in users
    ]
