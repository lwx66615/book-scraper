from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


class NovelBase(BaseModel):
    title: str
    author: Optional[str] = None
    source_url: str
    source_site: Optional[str] = None
    cover_url: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = "连载中"
    tags: Optional[str] = None


class NovelCreate(NovelBase):
    pass


class NovelUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    cover_url: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    tags: Optional[str] = None


class NovelResponse(NovelBase):
    id: int
    total_chapters: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class NovelListResponse(BaseModel):
    items: List[NovelResponse]
    total: int
    page: int
    page_size: int


class NovelDetailResponse(NovelResponse):
    chapters_count: int = 0
    reading_progress: Optional[dict] = None
