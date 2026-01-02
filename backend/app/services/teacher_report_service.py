from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.progress import Progress
from app.models.tests import Test
from app.models.assignments import Assignment


async def get_student_report(
    student_id: int,
    db: AsyncSession,
) -> dict:
    progress = await db.execute(
        select(Progress).where(Progress.user_id == student_id)
    )
    progress = progress.scalar_one_or_none()

    tests = await db.execute(
        select(Test).where(Test.created_by == student_id)
    )
    assignments = await db.execute(
        select(Assignment).where(Assignment.created_by == student_id)
    )

    return {
        "student_id": student_id,
        "progress": progress,
        "tests_attempted": tests.scalars().all(),
        "assignments": assignments.scalars().all(),
    }
