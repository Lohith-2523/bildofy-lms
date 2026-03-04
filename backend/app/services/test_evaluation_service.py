from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from app.models.test import Test
from app.models.test_question import TestQuestion
from app.models.test_attempt import TestAttempt
from app.models.test_answer import TestAnswer
from app.models.user import User
from app.services.xp_service import apply_xp_event


async def evaluate_test_submission(
    test_id: int,
    submitted_answers: list[dict],
    db: AsyncSession,
    current_user: User,
):
    result = await db.execute(
        select(Test).where(Test.id == test_id)
    )
    test = result.scalar_one_or_none()

    if not test:
        raise HTTPException(status_code=404, detail="Test not found")

    result = await db.execute(
        select(TestQuestion).where(TestQuestion.test_id == test_id)
    )
    questions = result.scalars().all()

    if not questions:
        raise HTTPException(status_code=400, detail="No questions found")

    # Ensure stable order
    questions = sorted(questions, key=lambda q: q.question_order)

    question_map = {q.id: q for q in questions}

    attempt = TestAttempt(
        test_id=test_id,
        student_id=current_user.id,
        score=0,
        percentage=0.0,
    )

    db.add(attempt)
    await db.flush()

    correct_count = 0
    results = []

    for submission in submitted_answers:
        qid = submission.question_id
        selected = submission.selected_answer

        if qid not in question_map:
            raise HTTPException(status_code=400, detail="Invalid question")

        question = question_map[qid]
        is_correct = selected == question.correct_answer

        if is_correct:
            correct_count += 1

        db.add(
            TestAnswer(
                test_attempt_id=attempt.id,
                question_id=qid,
                selected_answer=selected,
                is_correct=is_correct,
            )
        )

        # Build result entry
        question_index = questions.index(question)

        results.append({
            "question_index": question_index,
            "is_correct": is_correct,
            "correct_answer": question.correct_answer,
        })

    total = len(questions)
    percentage = (correct_count / total) * 100 if total else 0

    attempt.score = correct_count
    attempt.percentage = percentage
    xp_awarded = 100
    await db.flush()
    await apply_xp_event(
        user_id=current_user.id,
        event="TEST_COMPLETED",
        db=db,
    )

    await db.commit()

    return {
        "score": correct_count,
        "total_questions": total,
        "percentage": round(percentage, 2),
        "xp_awarded": xp_awarded,
        "results": results,
    }

