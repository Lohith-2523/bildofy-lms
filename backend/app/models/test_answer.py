from sqlalchemy import Column, Integer, ForeignKey, String, Boolean
from sqlalchemy.orm import relationship

from app.db.session import Base


class TestAnswer(Base):
    __tablename__ = "test_answers"

    id = Column(Integer, primary_key=True, index=True)

    test_attempt_id = Column(
        Integer,
        ForeignKey("test_attempts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    question_id = Column(Integer, nullable=False)
    
    selected_answer = Column(String(length=255), nullable=False)

    is_correct = Column(Boolean, nullable=False)
