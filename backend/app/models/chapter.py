from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Chapter(Base):
    __tablename__ = "chapters"

    id = Column(Integer, primary_key=True, index=True)
    novel_id = Column(Integer, ForeignKey("novels.id"), nullable=False)
    chapter_index = Column(Integer, nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text)
    source_url = Column(String(500))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    novel = relationship("Novel", back_populates="chapters")
