from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, case
from app.models.test_attempt import TestAttempt
from app.models.test import Test
from app.models.user import User
from app.models.subject import Subject
from app.models.attendance import AttendanceRecord
from app.services.analytics_student_service import StudentAnalyticsService

class AnalyticsService:
    """
    Centralized read-only analytics service.
    Uses BOTH score and percentage.
    """

    @staticmethod
    async def _student_attendance_percentage(db: AsyncSession, student_id: int) -> float:
        result = await db.execute(
            select(
                func.count(AttendanceRecord.id).label("total"),
                func.sum(case((AttendanceRecord.present == True, 1), else_=0)).label("present"),
            ).where(AttendanceRecord.student_id == student_id)
        )
        row = result.one()
        total = int(row.total or 0)
        present = int(row.present or 0)
        return round((present / total) * 100, 2) if total else 0.0

    @staticmethod
    async def _class_attendance_percentage(db: AsyncSession, class_id: int | None) -> float:
        if class_id is None:
            return 0.0

        result = await db.execute(
            select(
                func.count(AttendanceRecord.id).label("total"),
                func.sum(case((AttendanceRecord.present == True, 1), else_=0)).label("present"),
            )
            .join(User, User.id == AttendanceRecord.student_id)
            .where(User.class_id == class_id)
        )
        row = result.one()
        total = int(row.total or 0)
        present = int(row.present or 0)
        return round((present / total) * 100, 2) if total else 0.0

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
        attendance_percentage = await AnalyticsService._student_attendance_percentage(
            db=db,
            student_id=student_id,
        )

        return {
            "attempts": row.attempts or 0,
            "average_score": round(row.avg_score or 0, 2),
            "average_percentage": round(row.avg_percentage or 0, 2),
            "attendance_percentage": attendance_percentage,
        }

    @staticmethod
    async def class_overview(db: AsyncSession, class_id: int | None) -> dict:
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
        attendance_percentage = await AnalyticsService._class_attendance_percentage(
            db=db,
            class_id=class_id,
        )

        return {
            "students": row.students or 0,
            "average_score": round(row.avg_score or 0, 2),
            "average_percentage": round(row.avg_percentage or 0, 2),
            "attendance_percentage": attendance_percentage,
        }

    @staticmethod
    async def subject_overview(db: AsyncSession, teacher_id: int | None = None) -> list[dict]:
        tests_query = (
            select(
                Subject.id.label("subject_id"),
                Subject.name.label("subject_name"),
                func.avg(TestAttempt.score).label("avg_score"),
                func.avg(TestAttempt.percentage).label("avg_percentage"),
                func.count(TestAttempt.id).label("attempts"),
            )
            .join(Test, Test.id == TestAttempt.test_id)
            .join(Subject, Subject.id == Test.subject_id)
        )
        if teacher_id is not None:
            tests_query = tests_query.where(Subject.teacher_id == teacher_id)
        tests_query = tests_query.group_by(Subject.id, Subject.name)

        attendance_query = select(
            Subject.id.label("subject_id"),
            func.count(AttendanceRecord.id).label("total"),
            func.sum(case((AttendanceRecord.present == True, 1), else_=0)).label("present"),
        ).join(AttendanceRecord, AttendanceRecord.subject_id == Subject.id)
        if teacher_id is not None:
            attendance_query = attendance_query.where(Subject.teacher_id == teacher_id)
        attendance_query = attendance_query.group_by(Subject.id)

        test_rows = (await db.execute(tests_query)).all()
        attendance_rows = (await db.execute(attendance_query)).all()
        attendance_by_subject = {
            row.subject_id: round((int(row.present or 0) / int(row.total or 1)) * 100, 2)
            if int(row.total or 0) > 0
            else 0.0
            for row in attendance_rows
        }

        return [
            {
                "subject_id": row.subject_id,
                "subject": row.subject_name,
                "average_score": round(row.avg_score or 0, 2),
                "average_percentage": round(row.avg_percentage or 0, 2),
                "attempts": row.attempts,
                "attendance_percentage": attendance_by_subject.get(row.subject_id, 0.0),
            }
            for row in test_rows
        ]
