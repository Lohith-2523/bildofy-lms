from pydantic import BaseModel


class UserBase(BaseModel):
    id: int
    role: str
    name: str | None = None
    email: str
    grade: str | None = None
    board: str | None = None


class UserResponse(UserBase):
    pass
