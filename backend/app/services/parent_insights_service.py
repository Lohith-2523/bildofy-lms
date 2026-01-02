from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.progress import Progress
from app.ai import OllamaClient

ollama = OllamaClient()


async def get_parent_insights(
    student_id: int,
    db: AsyncSession,
) -> dict:
    """
    Generates read-only academic insights for parents.
    """

    result = await db.execute(
        select(Progress).where(Progress.user_id == student_id)
    )
    progress = result.scalar_one_or_none()

    if not progress:
        return {"insights": "No data available yet."}

    prompt = f"""
You are an educational analyst.

Analyze this student's academic progress and provide insights
for parents in simple, reassuring language.

XP: {progress.xp}
Level: {progress.level}
Stats: {progress.stats}

Rules:
- No recommendations to change syllabus
- No grading judgments
- Supportive tone
"""

    response = await ollama.generate(
        prompt=prompt,
        model_name="mistral:7b-instruct",
        temperature=0.2,
        max_tokens=600,
    )

    return {"insights": response}
