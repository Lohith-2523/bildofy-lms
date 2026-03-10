from pydantic import BaseModel, EmailStr
from typing import Optional
from app.security.roles import Role


class SignupRequest(BaseModel):
    name: Optional[str] = None
    email: EmailStr
    password: str
    role: str  # student | teacher
    registration_code: Optional[str] = None  # student only


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    role: Role
    class_id: Optional[int]
