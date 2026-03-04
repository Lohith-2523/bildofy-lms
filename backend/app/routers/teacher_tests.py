from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.security import get_current_user
from app.models.user import User, UserRole
from app.models.subject import Subject
from app.models.test import Test
from app.models.test_attempt import TestAttempt
from app.schemas.teacher_results import StudentTestResult


router = APIRouter(prefix="/teacher/tests", tags=["Teacher Tests"])


@router.get(
    "/subject/{subject_id}/results",
    response_model=list[StudentTestResult],
)
async def get_subject_results(
    subject_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # -------------------------------------------------
    # Role check
    # -------------------------------------------------
    if current_user.role != UserRole.teacher:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only teachers can view test results",
        )

    # -------------------------------------------------
    # Validate subject ownership
    # -------------------------------------------------
    subject_result = await db.execute(
        select(Subject).where(
            Subject.id == subject_id,
            Subject.teacher_id == current_user.id,
        )
    )
    subject = subject_result.scalar_one_or_none()

    if not subject:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subject not found or not assigned to teacher",
        )

    # -------------------------------------------------
    # Fetch tests for subject
    # -------------------------------------------------
    tests_result = await db.execute(
        select(Test).where(Test.subject == subject.name)
    )
    tests = tests_result.scalars().all()

    if not tests:
        return []

    test_ids = [t.id for t in tests]

    # -------------------------------------------------
    # Fetch attempts + student info
    # -------------------------------------------------
    attempts_result = await db.execute(
        select(
            TestAttempt,
            User.id,
            User.name,
            Test.title,
        )
        .join(User, User.id == TestAttempt.student_id)
        .join(Test, Test.id == TestAttempt.test_id)
        .where(TestAttempt.test_id.in_(test_ids))
    )

    results: list[StudentTestResult] = []

    for attempt, student_id, student_name, test_title in attempts_result.all():
        results.append(
            StudentTestResult(
                student_id=student_id,
                student_name=student_name,
                test_id=attempt.test_id,
                test_title=test_title,
                score=attempt.score,
                submitted_at=attempt.submitted_at,
            )
        )

    return results
