from pydantic import BaseModel
from datetime import datetime
from typing import Literal, Optional


class AssignmentCreateRequest(BaseModel):
    title: str
    subject: str
    description: Optional[str] = None
    due_date: datetime


class AssignmentResponse(BaseModel):
    id: int
    title: str
    subject: str
    due_date: datetime


class TeacherAssignmentCreateRequest(BaseModel):
    title: str
    subject: str
    due_date: datetime
    mode: Literal["LMS", "PDF"]
    content: Optional[str] = None


class StudentAssignmentListItem(BaseModel):
    id: int
    title: str
    subject: str
    due_date: datetime
    mode: Literal["LMS", "PDF"]
