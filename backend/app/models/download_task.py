from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class DownloadTask(Base):
    __tablename__ = "download_tasks"

    id = Column(Integer, primary_key=True, index=True)
    novel_id = Column(Integer, ForeignKey("novels.id"))
    status = Column(String(20), default="pending")  # pending/running/paused/completed/failed
    total_chapters = Column(Integer, default=0)
    downloaded_chapters = Column(Integer, default=0)
    current_chapter = Column(String(255))
    error_message = Column(Text)
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    novel = relationship("Novel", back_populates="download_tasks")
