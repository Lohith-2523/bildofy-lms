from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from app.db.session import Base


class GeneratedNote(Base):
    __tablename__ = "generated_notes"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    subject = Column(String(100), nullable=False)
    chapter = Column(String(200), nullable=False)
    difficulty = Column(String(20), nullable=False)

    pdf_url = Column(String(500), nullable=False)

    # 🔑 renamed from `metadata`
    extra_data = Column(JSON, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
