from pydantic import BaseModel
from typing import List


class QuestionResult(BaseModel):
    question_index: int
    is_correct: bool


class AnswerSubmission(BaseModel):
    question_id: int
    selected_answer: str


class TestSubmissionRequest(BaseModel):
    answers: list[AnswerSubmission]


class TestSubmissionResponse(BaseModel):
    score: int
    total_questions: int
    percentage: int
    results: List[QuestionResult]
