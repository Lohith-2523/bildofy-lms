from sqlalchemy.ext.asyncio import AsyncSession
from app.models.tests import Test
from app.schemas.tests import TestCreateRequest, TestResponse
from app.ai import OllamaClient

ollama = OllamaClient()


async def create_test_manual(
    payload: TestCreateRequest,
    db: AsyncSession,
) -> TestResponse:
    test = Test(
        created_by=1,  # teacher_id
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


async def create_test_ai_assisted(
    payload: TestCreateRequest,
    db: AsyncSession,
) -> TestResponse:
    prompt = f"""
You are assisting a teacher.
Suggest exam-style questions WITH answers.

Subject: {payload.subject}
Difficulty: {payload.difficulty}

Rules:
- Multiple choice
- Include correct answer
- Teacher will review
"""

    ai_output = await ollama.generate(
        prompt=prompt,
        model_name="mistral:7b-instruct",
        temperature=0.4,
        max_tokens=1200,
    )

    test = Test(
        created_by=1,
        title=payload.title,
        subject=payload.subject,
        difficulty=payload.difficulty,
        questions={"suggested": ai_output},
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
