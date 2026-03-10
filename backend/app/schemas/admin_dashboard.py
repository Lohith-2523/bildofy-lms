from pydantic import BaseModel, EmailStr
from typing import List, Optional, Literal, Dict, Any


class CreateTeacherRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    class_id: Optional[int] = None
    subject_ids: List[int] = []


class SubjectSeed(BaseModel):
    name: str
    teacher_id: int
    type: Literal["core", "extracurricular"]


class CreateClassRequest(BaseModel):
    grade: int
    section: str
    code_prefix: str
    subjects: List[SubjectSeed] = []


class ReassignClassRequest(BaseModel):
    user_id: int
    class_id: Optional[int] = None


class AssignTeacherSubjectRequest(BaseModel):
    subject_id: int
    teacher_id: int


class InfrastructureConfigRequest(BaseModel):
    boards: List[str]
    grades: List[int]
    subject_mapping: Dict[str, Any]
    chapter_metadata: Dict[str, Any]
