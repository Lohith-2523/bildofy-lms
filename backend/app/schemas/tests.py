from pydantic import BaseModel
from typing import List, Literal, Optional


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


class TeacherQuestionCreate(BaseModel):
    question: str
    question_type: Literal["MCQ", "SUBJECTIVE"]
    options: List[str] = []
    correct_answer: str


class TeacherManualTestCreateRequest(BaseModel):
    title: str
    subject_id: int
    difficulty: str = "medium"
    questions: List[TeacherQuestionCreate]


class TeacherAISuggestQuestionRequest(BaseModel):
    subject: str
    chapter: str
    difficulty: str = "medium"
    question_type: Literal["MCQ", "SUBJECTIVE"] = "MCQ"
    context: Optional[dict] = None


class TeacherAISuggestQuestionResponse(BaseModel):
    question: str
    question_type: Literal["MCQ", "SUBJECTIVE"]
    options: List[str] = []
    correct_answer: str
