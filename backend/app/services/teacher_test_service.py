from sqlalchemy.ext.asyncio import AsyncSession
from app.models.test import Test
from app.schemas.tests import TestCreateRequest, TestResponse
from app.ai import OllamaClient
from app.security import get_current_user
from app.models.user import User
from app.models.test_question import TestQuestion

from sqlalchemy import select
from fastapi import HTTPException
from app.models.subject import Subject

import json
from fastapi import Depends
import re

ollama = OllamaClient()


async def create_test_manual(
    payload: TestCreateRequest,
    db: AsyncSession,
    current_user: User =Depends(get_current_user),
) -> TestResponse:
    test = Test(
        created_by=current_user.id,  # teacher_id
        title=payload.title,
        subject=payload.subject,
        difficulty=payload.difficulty,
        questions=[],  # manually provided later
        total_marks=100,
    )

    db.add(test)
    await db.commit()
    await db.refresh(test)

    return TestResponse(
        test_id=test.id,
        title=test.title,
        total_marks=test.total_marks,
    )

def parse_ai_json_safely(raw: str):
    """
    Extracts and parses JSON array from LLM output.
    Preserves LaTeX/KaTeX content.
    """

    raw = raw.strip()

    # Remove markdown fences
    raw = re.sub(r"^```(?:json)?", "", raw)
    raw = re.sub(r"```$", "", raw)

    # Extract JSON array
    start = raw.find("[")
    end = raw.rfind("]")

    if start == -1 or end == -1:
        raise ValueError("AI did not return a valid JSON array.")

    candidate = raw[start:end + 1]

    try:
        return json.loads(candidate)
    except json.JSONDecodeError as e:
        print("AI RAW OUTPUT:\n", candidate)
        raise ValueError(f"Malformed AI JSON: {e}")


async def create_test_ai_assisted(
    payload,
    db: AsyncSession,
    current_user: User,
):
    # 🔹 1. Validate subject_id
    result = await db.execute(
        select(Subject).where(Subject.id == payload.subject_id)
    )
    subject = result.scalar_one_or_none()

    if not subject:
        raise HTTPException(status_code=400, detail="Invalid subject_id")

    # 🔹 2. Build AI prompt using REAL fields
    prompt = f"""
Generate multiple choice questions for:

Subject: {payload.subject}
Chapter: {payload.chapter}
Difficulty: {payload.difficulty}

Return ONLY valid JSON in this format:

[
  {{
    "question": "...",
    "options": ["A", "B", "C", "D"],
    "correct_answer": "..."
  }}
]

Ensure valid JSON. Escape inner quotes properly.
"""

    # 🔹 3. Call AI
    raw = await ollama.generate(
        model_name="mistral:7b-instruct",
        prompt=prompt,
        temperature=0.3,
        max_tokens=1200,
    )

    questions_data = parse_ai_json_safely(raw)

    if not isinstance(questions_data, list) or len(questions_data) == 0:
        raise HTTPException(status_code=400, detail="AI returned invalid questions")

    # 🔹 4. Create Test
    test = Test(
        title=payload.title,
        subject_id=payload.subject_id,
        created_by_student_id=current_user.id,
        difficulty=payload.difficulty,
        total_questions=len(questions_data),
    )

    db.add(test)
    await db.flush()

    # 🔹 5. Insert TestQuestion rows
    for index, q in enumerate(questions_data):
        if (
            "question" not in q
            or "options" not in q
            or "correct_answer" not in q
        ):
            raise HTTPException(status_code=400, detail="Malformed AI question")

        question_row = TestQuestion(
            test_id=test.id,
            question_text=q["question"],   # KaTeX preserved
            options=q["options"],
            correct_answer=q["correct_answer"],
            question_order=index,
        )

        db.add(question_row)

    await db.commit()
    await db.refresh(test)

    return test