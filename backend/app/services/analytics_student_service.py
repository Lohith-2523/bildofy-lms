from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.test_attempt import TestAttempt
from app.models.user import User


class StudentAnalyticsService:
    @staticmethod
    async def class_students_overview(
        db: AsyncSession,
        class_id: int,
    ) -> list[dict]:
        result = await db.execute(
            select(
                User.id,
                User.name,
                func.count(TestAttempt.id).label("attempts"),
                func.avg(TestAttempt.score).label("avg_score"),
                func.avg(TestAttempt.percentage).label("avg_percentage"),
            )
            .join(TestAttempt, TestAttempt.student_id == User.id, isouter=True)
            .where(User.class_id == class_id)
            .group_by(User.id)
        )

        return [
            {
                "student_id": r.id,
                "name": r.name,
                "attempts": r.attempts or 0,
                "average_score": round(r.avg_score or 0, 2),
                "average_percentage": round(r.avg_percentage or 0, 2),
            }
            for r in result.all()
        ]
