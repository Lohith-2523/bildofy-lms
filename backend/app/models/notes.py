from sqlalchemy import Column, Integer, String, DateTime, Boolean, JSON, ForeignKey
from sqlalchemy.sql import func
from app.db.session import Base


class GeneratedNote(Base):
    __tablename__ = "generated_notes"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    subject = Column(String(255), nullable=False)
    chapter = Column(String(255), nullable=False)
    difficulty = Column(String(50), nullable=False)

    content = Column(String, nullable=False)  # KaTeX-safe raw markdown

    is_saved = Column(Boolean, default=False)
    is_synced = Column(Boolean, default=False)

    is_student_generated = Column(Boolean, default=True)
    is_teacher_provided = Column(Boolean, default=False)

    extra_data = Column(JSON, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
