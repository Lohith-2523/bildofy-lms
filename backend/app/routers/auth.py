from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.auth import SignupRequest, LoginRequest, AuthResponse
from app.services.auth_service import signup_user, login_user
from sqlalchemy import select
from app.models.user import User
from app.security.jwt import create_access_token, create_refresh_token
from jose import JWTError
from app.security.passwords import verify_password

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/signup")
async def signup(
    data: SignupRequest,
    db: AsyncSession = Depends(get_db),
):
    user = await signup_user(data, db)
    return {"id": user.id, "role": user.role}


@router.post("/login")
async def login(payload: dict, db: AsyncSession = Depends(get_db)):
    email = payload.get("email")
    password = payload.get("password")

    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(
        {"sub": str(user.id), "role": user.role}
    )
    refresh_token = create_refresh_token(
        {"sub": str(user.id)}
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "role": user.role,
            "class_id": user.class_id,
        },
    }


@router.post("/refresh")
async def refresh(payload: dict):
    from app.security.jwt import decode_token

    token = payload.get("refresh_token")

    try:
        data = decode_token(token)
        if data.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        user_id = data.get("sub")
        access_token = create_access_token({"sub": user_id})

        return {"access_token": access_token}
    except JWTError:
        raise HTTPException(status_code=401, detail="Expired refresh token")