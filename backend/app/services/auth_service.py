from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

from app.models.user import User, UserRole
from app.models.classroom import Classroom
from app.models.progress import Progress
from app.schemas.auth import SignupRequest, LoginRequest
from app.security.passwords import hash_password, verify_password
from app.security.jwt import create_access_token

def parse_registration_code(code: str):
    if len(code) != 6 or not code.isdigit():
        raise HTTPException(status_code=400, detail="Invalid registration code")

    grade = int(code[:2])
    section_num = code[2:4]
    roll = int(code[4:])

    section_map = {"01": "A", "02": "B", "03": "C"}
    if section_num not in section_map:
        raise HTTPException(status_code=400, detail="Invalid section code")

    return grade, section_map[section_num], roll


async def signup_user(payload: SignupRequest, db: AsyncSession):
    result = await db.execute(select(User).where(User.email == payload.email))
    if result.scalar():
        raise HTTPException(status_code=400, detail="Email already registered")

    class_id = None

    if payload.role == "student":
        if not payload.registration_code:
            raise HTTPException(status_code=400, detail="Registration code required")

        grade, section, _ = parse_registration_code(payload.registration_code)
        prefix = payload.registration_code[:4]

        result = await db.execute(
            select(Classroom).where(Classroom.code_prefix == prefix)
        )
        classroom = result.scalar()

        if not classroom:
            classroom = Classroom(
                grade=grade,
                section=section,
                code_prefix=prefix,
            )
            db.add(classroom)
            await db.flush()

        class_id = classroom.id

    user = User(
        email=payload.email,
        password_hash=hash_password(payload.password),
        role=UserRole(payload.role),
        class_id=class_id,
    )
    db.add(user)
    await db.flush()

    if payload.role == "student":
        progress = Progress(user_id=user.id)
        db.add(progress)

    await db.commit()

    return {
        "user_id": user.id,
        "role": user.role.value,
        "class_id": user.class_id,
    }


async def login_user(data: LoginRequest, db: AsyncSession):
    result = await db.execute(select(User).where(User.email == data.email))
    user = result.scalar_one_or_none()

    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token({
        "sub": user.id,
        "role": user.role,
        "class_id": user.class_id
    })

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "role": user.role,
        "class_id": user.class_id
    }