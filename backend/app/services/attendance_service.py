from datetime import date

from fastapi import HTTPException
from sqlalchemy import case, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.attendance import AttendanceRecord
from app.models.subject import Subject, SubjectType
from app.models.subject_student import SubjectStudent
from app.models.user import User, UserRole
from app.schemas.attendance import AttendanceMarkRequest


async def _get_teacher_subject(
    db: AsyncSession,
    teacher_id: int,
    subject_id: int,
) -> Subject:
    result = await db.execute(
        select(Subject).where(
            Subject.id == subject_id,
            Subject.teacher_id == teacher_id,
        )
    )
    subject = result.scalar_one_or_none()
    if subject is None:
        raise HTTPException(status_code=404, detail="Subject not found for this teacher")
    return subject


async def teacher_subject_students(
    db: AsyncSession,
    teacher_id: int,
    subject_id: int,
):
    subject = await _get_teacher_subject(db, teacher_id, subject_id)

    if subject.type == SubjectType.core and subject.class_id is not None:
        result = await db.execute(
            select(User).where(
                User.role == UserRole.student,
                User.class_id == subject.class_id,
            )
        )
        students = result.scalars().all()
    else:
        result = await db.execute(
            select(User)
            .join(SubjectStudent, SubjectStudent.student_id == User.id)
            .where(
                SubjectStudent.subject_id == subject.id,
                User.role == UserRole.student,
            )
        )
        students = result.scalars().all()

    return subject, students


async def get_teacher_attendance_roster(
    db: AsyncSession,
    teacher_id: int,
    subject_id: int,
    attendance_date: date,
):
    subject, students = await teacher_subject_students(db, teacher_id, subject_id)
    student_ids = [s.id for s in students]

    attendance_map: dict[int, AttendanceRecord] = {}
    if student_ids:
        records_result = await db.execute(
            select(AttendanceRecord).where(
                AttendanceRecord.subject_id == subject.id,
                AttendanceRecord.attendance_date == attendance_date,
                AttendanceRecord.student_id.in_(student_ids),
            )
        )
        records = records_result.scalars().all()
        attendance_map = {r.student_id: r for r in records}

    return [
        {
            "student_id": s.id,
            "name": s.name or f"Student {s.id}",
            "present": attendance_map.get(s.id).present if s.id in attendance_map else None,
            "remark": attendance_map.get(s.id).remark if s.id in attendance_map else None,
        }
        for s in students
    ]


async def mark_attendance(
    db: AsyncSession,
    teacher_id: int,
    payload: AttendanceMarkRequest,
):
    subject, students = await teacher_subject_students(db, teacher_id, payload.subject_id)
    valid_student_ids = {s.id for s in students}

    updated = 0
    created = 0
    for item in payload.records:
        if item.student_id not in valid_student_ids:
            continue

        existing_result = await db.execute(
            select(AttendanceRecord).where(
                AttendanceRecord.student_id == item.student_id,
                AttendanceRecord.subject_id == subject.id,
                AttendanceRecord.attendance_date == payload.attendance_date,
            )
        )
        existing = existing_result.scalar_one_or_none()

        if existing:
            existing.present = item.present
            existing.remark = item.remark
            updated += 1
        else:
            db.add(
                AttendanceRecord(
                    student_id=item.student_id,
                    teacher_id=teacher_id,
                    subject_id=subject.id,
                    class_id=subject.class_id,
                    attendance_date=payload.attendance_date,
                    present=item.present,
                    remark=item.remark,
                )
            )
            created += 1

    await db.commit()
    return {
        "ok": True,
        "created": created,
        "updated": updated,
        "subject_id": subject.id,
        "attendance_date": payload.attendance_date,
    }


async def student_attendance_records(
    db: AsyncSession,
    student_id: int,
):
    result = await db.execute(
        select(
            AttendanceRecord.attendance_date,
            AttendanceRecord.subject_id,
            Subject.name.label("subject_name"),
            AttendanceRecord.present,
            AttendanceRecord.remark,
        )
        .join(Subject, Subject.id == AttendanceRecord.subject_id)
        .where(AttendanceRecord.student_id == student_id)
        .order_by(AttendanceRecord.attendance_date.desc())
    )
    rows = result.all()
    return [
        {
            "attendance_date": r.attendance_date,
            "subject_id": r.subject_id,
            "subject_name": r.subject_name,
            "present": r.present,
            "remark": r.remark,
        }
        for r in rows
    ]


async def student_attendance_summary(
    db: AsyncSession,
    student_id: int,
):
    overall_result = await db.execute(
        select(
            func.count(AttendanceRecord.id).label("total"),
            func.sum(case((AttendanceRecord.present == True, 1), else_=0)).label("present"),
        ).where(AttendanceRecord.student_id == student_id)
    )
    overall = overall_result.one()
    total = int(overall.total or 0)
    present = int(overall.present or 0)
    percentage = round((present / total) * 100, 2) if total else 0.0

    by_subject_result = await db.execute(
        select(
            Subject.id.label("subject_id"),
            Subject.name.label("subject_name"),
            func.count(AttendanceRecord.id).label("total"),
            func.sum(case((AttendanceRecord.present == True, 1), else_=0)).label("present"),
        )
        .join(Subject, Subject.id == AttendanceRecord.subject_id)
        .where(AttendanceRecord.student_id == student_id)
        .group_by(Subject.id, Subject.name)
        .order_by(Subject.name)
    )
    subject_rows = by_subject_result.all()

    return {
        "overall": {
            "total": total,
            "present": present,
            "absent": max(total - present, 0),
            "percentage": percentage,
        },
        "subjects": [
            {
                "subject_id": r.subject_id,
                "subject_name": r.subject_name,
                "total": int(r.total or 0),
                "present": int(r.present or 0),
                "absent": max(int((r.total or 0) - (r.present or 0)), 0),
                "percentage": round((int(r.present or 0) / int(r.total or 1)) * 100, 2)
                if int(r.total or 0) > 0
                else 0.0,
            }
            for r in subject_rows
        ],
    }
