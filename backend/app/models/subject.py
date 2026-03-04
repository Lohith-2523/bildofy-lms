from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
import enum
from datetime import datetime

from app.db.session import Base


class SubjectType(str, enum.Enum):
    core = "core"
    elective = "elective"
    extracurricular = "extracurricular"


class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
    type = Column(Enum(SubjectType), nullable=False)

    # Core subjects only
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=True)

    # Exactly one teacher
    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # 🔽 Phase 2.4 additions (nullable by design)
    max_students = Column(Integer, nullable=True)
    enrollment_open_at = Column(DateTime, nullable=True)
    enrollment_close_at = Column(DateTime, nullable=True)

    teacher = relationship("User", foreign_keys=[teacher_id])
