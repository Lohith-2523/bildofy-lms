from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.progress import Progress
from app.models.assignments import Assignment
from app.models.tests import Test


async def get_parent_overview(
    student_id: int,
    db: AsyncSession,
) -> dict:
    """
    High-level snapshot for parents.
    """

    progress_result = await db.execute(
        select(Progress).where(Progress.user_id == student_id)
    )
    progress = progress_result.scalar_one_or_none()

    assignments_result = await db.execute(
        select(Assignment).where(Assignment.created_by == student_id)
    )
    assignments = assignments_result.scalars().all()

    tests_result = await db.execute(
        select(Test).where(Test.created_by == student_id)
    )
    tests = tests_result.scalars().all()

    return {
        "student_id": student_id,
        "xp": progress.xp if progress else 0,
        "level": progress.level if progress else 1,
        "assignments_assigned": len(assignments),
        "tests_attempted": len(tests),
    }


async def get_detailed_progress(
    student_id: int,
    db: AsyncSession,
) -> dict:
    """
    Detailed academic breakdown.
    """

    progress_result = await db.execute(
        select(Progress).where(Progress.user_id == student_id)
    )
    progress = progress_result.scalar_one_or_none()

    return {
        "student_id": student_id,
        "xp": progress.xp if progress else 0,
        "level": progress.level if progress else 1,
        "stats": progress.stats if progress else {},
    }
