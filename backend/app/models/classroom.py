from sqlalchemy import Column, Integer, String
from app.db.session import Base


class Classroom(Base):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, index=True)
    grade = Column(Integer, nullable=False)
    section = Column(String, nullable=False)  # A, B, C
    code_prefix = Column(String, unique=True, nullable=False)  # e.g. "1103"
