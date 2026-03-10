from pydantic import BaseModel
from typing import Optional
from enum import Enum


class SubjectType(str, Enum):
    core = "core"
    elective = "elective"
    extracurricular = "extracurricular"


class SubjectCreateRequest(BaseModel):
    name: str
    type: SubjectType
    class_id: Optional[int] = None
    teacher_id: int


class SubjectResponse(BaseModel):
    id: int
    name: str
    type: SubjectType
    class_id: Optional[int]
    teacher_id: int
