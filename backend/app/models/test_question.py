from sqlalchemy import Column, Integer, ForeignKey, Text, JSON, String
from sqlalchemy.orm import relationship

from app.db.session import Base


class TestQuestion(Base):
    __tablename__ = "test_questions"

    id = Column(Integer, primary_key=True, index=True)

    test_id = Column(
        Integer,
        ForeignKey("tests.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    test = relationship("Test", back_populates="questions")

    question_text = Column(Text, nullable=False)

    options = Column(JSON, nullable=False)

    correct_answer = Column(String(length=255), nullable=False)

    question_order = Column(Integer, nullable=False)
    