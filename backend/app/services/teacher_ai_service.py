from app.ai import OllamaClient, select_model
from app.schemas.common import ClientContext

ollama = OllamaClient()


async def suggest_test_questions(
    subject: str,
    difficulty: str,
    context: ClientContext,
) -> dict:
    model = select_model(context)

    prompt = f"""
Suggest exam-quality questions WITH answers.

Subject: {subject}
Difficulty: {difficulty}

Rules:
- Accurate
- Syllabus-aligned
- Teacher will review
"""

    response = await ollama.generate(
        prompt=prompt,
        model_name=model,
        temperature=0.35,
        max_tokens=1000,
    )

    return {"suggestions": response}


async def suggest_assignment_outline(
    subject: str,
    topic: str,
    context: ClientContext,
) -> dict:
    model = select_model(context)

    prompt = f"""
Create an assignment outline for students.

Subject: {subject}
Topic: {topic}

Rules:
- Clear objectives
- Structured tasks
"""

    response = await ollama.generate(
        prompt=prompt,
        model_name=model,
        temperature=0.3,
        max_tokens=800,
    )

    return {"outline": response}
