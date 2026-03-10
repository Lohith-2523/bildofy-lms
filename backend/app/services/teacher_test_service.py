import json
import re
from typing import Any

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai import OllamaClient
from app.models.subject import Subject
from app.models.test import Test
from app.models.test_question import TestQuestion
from app.models.user import User
from app.schemas.tests import (
    TeacherAISuggestQuestionResponse,
    TeacherManualTestCreateRequest,
    TestCreateRequest,
    TestResponse,
)

ollama = OllamaClient()


def parse_ai_json_safely(raw: str):
    raw = raw.strip()
    raw = re.sub(r"^```(?:json)?", "", raw)
    raw = re.sub(r"```$", "", raw)

    start = raw.find("[")
    end = raw.rfind("]")
    if start == -1 or end == -1:
        raise ValueError("AI did not return a valid JSON array.")
    return json.loads(raw[start:end + 1])


def _extract_json_object(raw: str) -> dict[str, Any]:
    cleaned = raw.strip()
    cleaned = re.sub(r"^```(?:json)?", "", cleaned)
    cleaned = re.sub(r"```$", "", cleaned).strip()

    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("AI did not return a valid JSON object.")

    return json.loads(cleaned[start:end + 1])


async def create_test_manual(
    payload: TeacherManualTestCreateRequest,
    db: AsyncSession,
    current_user: User,
) -> TestResponse:
    if not payload.questions:
        raise HTTPException(status_code=400, detail="At least one question is required")

    subject_result = await db.execute(
        select(Subject).where(Subject.id == payload.subject_id)
    )
    subject = subject_result.scalar_one_or_none()
    if not subject:
        raise HTTPException(status_code=400, detail="Invalid subject_id")

    test = Test(
        title=payload.title,
        subject_id=payload.subject_id,
        created_by_student_id=current_user.id,
        difficulty=payload.difficulty,
        total_questions=len(payload.questions),
    )
    db.add(test)
    await db.flush()

    for idx, q in enumerate(payload.questions):
        options = q.options if q.question_type == "MCQ" else []
        if q.question_type == "MCQ" and len(options) < 2:
            raise HTTPException(
                status_code=400,
                detail=f"MCQ question {idx + 1} requires at least 2 options",
            )

        db.add(
            TestQuestion(
                test_id=test.id,
                question_text=q.question,
                options=options,
                correct_answer=q.correct_answer,
                question_order=idx,
            )
        )

    await db.commit()
    await db.refresh(test)

    return TestResponse(
        test_id=test.id,
        title=test.title,
        total_marks=len(payload.questions),
    )


async def suggest_single_question(
    subject: str,
    chapter: str,
    difficulty: str,
    question_type: str,
) -> TeacherAISuggestQuestionResponse:
    prompt = f"""
Generate exactly one {question_type} question for:
Subject: {subject}
Chapter: {chapter}
Difficulty: {difficulty}

Return ONLY valid JSON object:
{{
  "question": "...",
  "question_type": "{question_type}",
  "options": ["..."] ,  // empty list for SUBJECTIVE
  "correct_answer": "..."
}}
"""

    raw = await ollama.generate(
        model_name="mistral:7b-instruct",
        prompt=prompt,
        temperature=0.3,
        max_tokens=700,
    )

    parsed = _extract_json_object(raw)
    return TeacherAISuggestQuestionResponse(
        question=str(parsed.get("question", "")).strip(),
        question_type="MCQ" if question_type == "MCQ" else "SUBJECTIVE",
        options=parsed.get("options") or [],
        correct_answer=str(parsed.get("correct_answer", "")).strip(),
    )


async def create_test_ai_assisted(
    payload: TestCreateRequest,
    db: AsyncSession,
    current_user: User,
):
    result = await db.execute(select(Subject).where(Subject.id == payload.subject_id))
    subject = result.scalar_one_or_none()
    if not subject:
        raise HTTPException(status_code=400, detail="Invalid subject_id")

    prompt = f"""
Generate multiple choice questions for:

Subject: {payload.subject}
Chapter: {payload.chapter}
Difficulty: {payload.difficulty}

Return ONLY valid JSON:
[
  {{
    "question": "...",
    "options": ["A", "B", "C", "D"],
    "correct_answer": "..."
  }}
]
"""

    raw = await ollama.generate(
        model_name="mistral:7b-instruct",
        prompt=prompt,
        temperature=0.3,
        max_tokens=1200,
    )
    questions_data = parse_ai_json_safely(raw)

    if not isinstance(questions_data, list) or not questions_data:
        raise HTTPException(status_code=400, detail="AI returned invalid questions")

    test = Test(
        title=payload.title,
        subject_id=payload.subject_id,
        created_by_student_id=current_user.id,
        difficulty=payload.difficulty,
        total_questions=len(questions_data),
    )
    db.add(test)
    await db.flush()

    for index, q in enumerate(questions_data):
        db.add(
            TestQuestion(
                test_id=test.id,
                question_text=q["question"],
                options=q["options"],
                correct_answer=q["correct_answer"],
                question_order=index,
            )
        )

    await db.commit()
    await db.refresh(test)
    return test
