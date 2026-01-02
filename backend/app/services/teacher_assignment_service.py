from sqlalchemy.ext.asyncio import AsyncSession
from app.models.assignments import Assignment
from app.schemas.assignments import AssignmentCreateRequest, AssignmentResponse


async def create_assignment(
    payload: AssignmentCreateRequest,
    assignment_type: str,
    db: AsyncSession,
) -> AssignmentResponse:
    assignment = Assignment(
        created_by=1,  # teacher_id (auth wired later)
        title=payload.title,
        subject=payload.subject,
        description=payload.description,
        due_date=payload.due_date,
    )

    # Store assignment type in metadata-like pattern (future-proof)
    assignment.metadata = {
        "assignment_type": assignment_type
    }

    db.add(assignment)
    await db.commit()
    await db.refresh(assignment)

    return AssignmentResponse(
        id=assignment.id,
        title=assignment.title,
        subject=assignment.subject,
        due_date=assignment.due_date,
    )
