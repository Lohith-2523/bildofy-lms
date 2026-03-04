from pydantic import BaseModel
from typing import List


class TestQuestion(BaseModel):
    question: str
    options: List[str]
    correct_option: int


class TestCreateRequest(BaseModel):
    title: str
    subject_id: int
    subject: str
    chapter: str
    difficulty: str
    ai_assisted: bool


class TestResponse(BaseModel):
    test_id: int
    title: str
    total_marks: int
