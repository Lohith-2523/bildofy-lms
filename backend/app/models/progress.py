from sqlalchemy import Column, Integer, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.session import Base


class Progress(Base):
    __tablename__ = "progress"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)

    xp = Column(Integer, default=0)
    level = Column(Integer, default=1)
    stats = Column(JSON, default=dict)
    updated_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="progress")
