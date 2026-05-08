from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class ReadingProgress(Base):
    __tablename__ = "reading_progress"

    id = Column(Integer, primary_key=True, index=True)
    novel_id = Column(Integer, ForeignKey("novels.id"), unique=True)
    last_chapter_id = Column(Integer)
    last_position = Column(Integer, default=0)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    novel = relationship("Novel", back_populates="reading_progress")
