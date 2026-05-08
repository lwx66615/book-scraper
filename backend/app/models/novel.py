from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Novel(Base):
    __tablename__ = "novels"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    author = Column(String(100))
    source_url = Column(String(500), nullable=False)
    source_site = Column(String(100))
    cover_url = Column(String(500))
    description = Column(Text)
    status = Column(String(20), default="连载中")
    tags = Column(String(500))
    total_chapters = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    chapters = relationship("Chapter", back_populates="novel", cascade="all, delete-orphan")
    download_tasks = relationship("DownloadTask", back_populates="novel", cascade="all, delete-orphan")
    reading_progress = relationship("ReadingProgress", back_populates="novel", uselist=False, cascade="all, delete-orphan")
