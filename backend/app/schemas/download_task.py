from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


class DownloadStartRequest(BaseModel):
    url: str
    tags: Optional[str] = None


class DownloadTaskResponse(BaseModel):
    id: int
    novel_id: int
    status: str
    total_chapters: int
    downloaded_chapters: int
    current_chapter: Optional[str] = None
    error_message: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class DownloadTaskListResponse(BaseModel):
    items: List[DownloadTaskResponse]
    total: int


class DownloadProgressResponse(BaseModel):
    task_id: int
    status: str
    progress: float  # 0-100
    downloaded_chapters: int
    total_chapters: int
    current_chapter: Optional[str] = None
