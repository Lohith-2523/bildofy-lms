from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.test_attempt import TestAttempt
from sqlalchemy.orm import selectinload
import io
from fpdf import FPDF

from app.db.session import get_db
from app.services.teacher_test_service import create_test_ai_assisted
from app.schemas.tests import TestCreateRequest
from app.security import get_current_user
from app.models.user import User, UserRole
from app.models.test import Test
from app.schemas.test_submission import (
    TestSubmissionRequest,
    TestSubmissionResponse,
)
from app.services.test_evaluation_service import evaluate_test_submission


router = APIRouter(prefix="/student/tests", tags=["Student Tests"])


@router.get("/{test_id}")
async def get_test_for_student(
    test_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Test)
        .options(selectinload(Test.questions))
        .where(Test.id == test_id)
    )

    test = result.scalar_one_or_none()

    if not test:
        raise HTTPException(status_code=404, detail="Test not found")

    questions = [
        {
            "id": q.id,
            "question": q.question_text,
            "options": q.options,
            "question_type": "MCQ" if q.options else "SUBJECTIVE",
        }
        for q in sorted(test.questions, key=lambda x: x.question_order)
    ]

    return {
        "id": test.id,
        "subject_id": test.subject_id,
        "difficulty": test.difficulty,
        "total_questions": test.total_questions,
        "questions": questions,
    }



@router.post(
    "/{test_id}/submit",
    response_model=TestSubmissionResponse,
)
async def submit_test(
    test_id: int,
    payload: TestSubmissionRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != UserRole.student:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only students can submit tests",
        )

    result = await evaluate_test_submission(
        test_id=test_id,
        submitted_answers=payload.answers,
        db=db,
        current_user=current_user,
    )

    return result


@router.get("")
async def list_tests_for_student(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != UserRole.student:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only students can view tests",
        )

    result = await db.execute(
        select(Test)
        .options(selectinload(Test.questions))
    )

    tests = result.scalars().all()

    response = []

    for t in tests:
        # Fetch attempts for this student & test
        attempts_result = await db.execute(
            select(
                func.max(TestAttempt.score),
                func.count(TestAttempt.id),
            ).where(
                TestAttempt.test_id == t.id,
                TestAttempt.student_id == current_user.id,
            )
        )
        best_score, attempt_count = attempts_result.one()

        questions = [
            {
                "id": q.id,
                "question": q.question_text,
                "options": q.options,
            }
            for q in t.questions
        ]


        response.append(
            {
                "id": t.id,
                "title": t.title,
                "subject_id": t.subject_id,
                "difficulty": t.difficulty,
                "total_questions": len(questions),
                "question_type": "MCQ" if all((q.options and len(q.options) > 0) for q in t.questions) else "SUBJECTIVE",

                # --------- Aggregated fields ---------
                "duration": len(questions),
                "xp_reward": 0,                 # XP shell untouched
                "is_completed": attempt_count > 0,
                "best_score": best_score,
            }
        )

    return response

@router.post("/generate")
async def generate_test_for_student(
    payload: dict,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != UserRole.student:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only students can generate tests",
        )

    subject_id = payload.get("subject_id")
    chapter = payload.get("chapter")
    subject = payload.get("subject")

    if not subject_id or not chapter:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="subject_id and chapter are required",
        )

    # Reuse existing AI-assisted test creation
    test_request = TestCreateRequest(
        title=f"Practice Test - {chapter}",
        subject_id=subject_id,
        subject = subject,
        difficulty="medium",
        chapter=chapter,
        ai_assisted=True,
    )

    test = await create_test_ai_assisted(test_request, db, current_user)
    return {"id": test.id, "title": test.title}


@router.get("/{test_id}/paper/pdf")
async def export_test_question_paper_pdf(
    test_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Test).options(selectinload(Test.questions)).where(Test.id == test_id)
    )
    test = result.scalar_one_or_none()
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Helvetica", "B", 16)
    pdf.multi_cell(0, 10, txt=test.title or "Test Paper")
    pdf.ln(2)
    pdf.set_font("Helvetica", "", 12)
    pdf.multi_cell(0, 8, txt=f"Difficulty: {test.difficulty}")
    pdf.multi_cell(0, 8, txt=f"Total Questions: {len(test.questions)}")
    pdf.ln(5)

    for idx, q in enumerate(sorted(test.questions, key=lambda x: x.question_order), 1):
        pdf.set_font("Helvetica", "B", 12)
        pdf.multi_cell(0, 8, txt=f"Q{idx}. {q.question_text}")
        if q.options:
            pdf.set_font("Helvetica", "", 11)
            for opt in q.options:
                pdf.multi_cell(0, 7, txt=f" - {opt}")
        pdf.ln(2)

    output = bytes(pdf.output(dest="S"))
    return StreamingResponse(
        io.BytesIO(output),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="test_{test_id}_paper.pdf"'
        },
    )


