from app.ai import OllamaClient
from app.schemas.tests import TestCreateRequest, TestResponse

ollama = OllamaClient()


async def generate_test(request: TestCreateRequest) -> TestResponse:
    prompt = f"""
Create an exam-style test.

Subject: {request.subject}
Difficulty: {request.difficulty}

Rules:
- Multiple choice
- One correct answer
- Clear options
"""

    response = await ollama.generate(
        prompt=prompt,
        model_name="mistral:7b-instruct",
        temperature=0.4,
        max_tokens=1500,
    )

    return TestResponse(
        test_id=1,
        title=request.title,
        total_marks=100,
    )
