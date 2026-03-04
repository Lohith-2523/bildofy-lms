from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base
import enum


class UserRole(str, enum.Enum):
    student = "student"
    teacher = "teacher"
    parent = "parent"
    admin = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    name = Column(String, nullable=True)
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=True)

    progress = relationship("Progress", back_populates="user", uselist=False)
    total_xp = Column(Integer, nullable=False, server_default="0")
    level = Column(Integer, nullable=False, server_default="1")

