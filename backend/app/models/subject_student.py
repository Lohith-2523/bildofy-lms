from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from app.db.session import Base


class SubjectStudent(Base):
    __tablename__ = "subject_students"

    id = Column(Integer, primary_key=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    __table_args__ = (
        UniqueConstraint("subject_id", "student_id", name="uq_subject_student"),
    )
