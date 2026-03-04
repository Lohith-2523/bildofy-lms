from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.test_attempt import TestAttempt
from app.models.test import Test
from app.models.user import User
from app.models.subject import Subject
from app.services.analytics_student_service import StudentAnalyticsService

class AnalyticsService:
    """
    Centralized read-only analytics service.
    Uses BOTH score and percentage.
    """

    @staticmethod
    async def student_overview(db: AsyncSession, student_id: int) -> dict:
        result = await db.execute(
            select(
                func.count(TestAttempt.id).label("attempts"),
                func.avg(TestAttempt.score).label("avg_score"),
                func.avg(TestAttempt.percentage).label("avg_percentage"),
            ).where(TestAttempt.student_id == student_id)
        )

        row = result.one()

        return {
            "attempts": row.attempts or 0,
            "average_score": round(row.avg_score or 0, 2),
            "average_percentage": round(row.avg_percentage or 0, 2),
        }

    @staticmethod
    async def class_overview(db: AsyncSession, class_id: int) -> dict:
        result = await db.execute(
            select(
                func.count(func.distinct(TestAttempt.student_id)).label("students"),
                func.avg(TestAttempt.score).label("avg_score"),
                func.avg(TestAttempt.percentage).label("avg_percentage"),
            )
            .join(User, User.id == TestAttempt.student_id)
            .where(User.class_id == class_id)
        )

        row = result.one()

        return {
            "students": row.students or 0,
            "average_score": round(row.avg_score or 0, 2),
            "average_percentage": round(row.avg_percentage or 0, 2),
        }

    @staticmethod
    async def subject_overview(db: AsyncSession) -> list[dict]:
        result = await db.execute(
            select(
                Subject.id.label("subject_id"),
                Subject.name.label("subject_name"),
                func.avg(TestAttempt.score).label("avg_score"),
                func.avg(TestAttempt.percentage).label("avg_percentage"),
                func.count(TestAttempt.id).label("attempts"),
            )
            .join(Test, Test.id == TestAttempt.test_id)
            .join(Subject, Subject.id == Test.subject_id)
            .group_by(Subject.id, Subject.name)
        )

        rows = result.all()

        return [
            {
                "subject_id": row.subject_id,
                "subject": row.subject_name,
                "average_score": round(row.avg_score or 0, 2),
                "average_percentage": round(row.avg_percentage or 0, 2),
                "attempts": row.attempts,
            }
            for row in rows
        ]