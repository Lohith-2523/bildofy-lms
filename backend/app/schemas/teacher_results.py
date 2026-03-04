from pydantic import BaseModel
from datetime import datetime


class StudentTestResult(BaseModel):
    student_id: int
    student_name: str
    test_id: int
    test_title: str
    score: int
    submitted_at: datetime
