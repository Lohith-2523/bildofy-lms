from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, case
from app.models.test_attempt import TestAttempt
from app.models.user import User
from app.models.subject import Subject, SubjectType
from app.models.subject_student import SubjectStudent
from app.models.user import UserRole
from app.models.attendance import AttendanceRecord


class StudentAnalyticsService:
    @staticmethod
    async def _attendance_map(
        db: AsyncSession,
        student_ids: list[int],
    ) -> dict[int, float]:
        if not student_ids:
            return {}

        result = await db.execute(
            select(
                AttendanceRecord.student_id,
                func.count(AttendanceRecord.id).label("total"),
                func.sum(case((AttendanceRecord.present == True, 1), else_=0)).label("present"),
            )
            .where(AttendanceRecord.student_id.in_(student_ids))
            .group_by(AttendanceRecord.student_id)
        )

        return {
            row.student_id: round((int(row.present or 0) / int(row.total or 1)) * 100, 2)
            if int(row.total or 0) > 0
            else 0.0
            for row in result.all()
        }

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

        rows = result.all()
        attendance_by_student = await StudentAnalyticsService._attendance_map(
            db=db,
            student_ids=[row.id for row in rows],
        )

        return [
            {
                "student_id": r.id,
                "name": (r.name or f"Student {r.id}"),
                "attempts": r.attempts or 0,
                "average_score": round(r.avg_score or 0, 2),
                "average_percentage": round(r.avg_percentage or 0, 2),
                "attendance_percentage": attendance_by_student.get(r.id, 0.0),
            }
            for r in rows
        ]

    @staticmethod
    async def teacher_students_overview(
        db: AsyncSession,
        teacher_id: int,
    ) -> list[dict]:
        subject_result = await db.execute(
            select(Subject).where(Subject.teacher_id == teacher_id)
        )
        subjects = subject_result.scalars().all()
        if not subjects:
            return []

        student_ids: set[int] = set()

        for subject in subjects:
            if subject.type == SubjectType.core and subject.class_id is not None:
                class_students = await db.execute(
                    select(User.id).where(
                        User.role == UserRole.student,
                        User.class_id == subject.class_id,
                    )
                )
                student_ids.update(class_students.scalars().all())
            else:
                enrolled = await db.execute(
                    select(SubjectStudent.student_id).where(
                        SubjectStudent.subject_id == subject.id
                    )
                )
                student_ids.update(enrolled.scalars().all())

        if not student_ids:
            return []

        result = await db.execute(
            select(
                User.id,
                User.name,
                func.count(TestAttempt.id).label("attempts"),
                func.avg(TestAttempt.score).label("avg_score"),
                func.avg(TestAttempt.percentage).label("avg_percentage"),
            )
            .join(TestAttempt, TestAttempt.student_id == User.id, isouter=True)
            .where(
                User.role == UserRole.student,
                User.id.in_(student_ids),
            )
            .group_by(User.id)
        )

        rows = result.all()
        attendance_by_student = await StudentAnalyticsService._attendance_map(
            db=db,
            student_ids=[row.id for row in rows],
        )

        return [
            {
                "student_id": r.id,
                "name": (r.name or f"Student {r.id}"),
                "attempts": r.attempts or 0,
                "average_score": round(r.avg_score or 0, 2),
                "average_percentage": round(r.avg_percentage or 0, 2),
                "attendance_percentage": attendance_by_student.get(r.id, 0.0),
            }
            for r in rows
        ]
