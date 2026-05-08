from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


class ChapterBase(BaseModel):
    chapter_index: int
    title: str
    source_url: Optional[str] = None


class ChapterCreate(ChapterBase):
    novel_id: int
    content: Optional[str] = None


class ChapterResponse(ChapterBase):
    id: int
    novel_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class ChapterContentResponse(ChapterResponse):
    content: Optional[str] = None


class ChapterListResponse(BaseModel):
    items: List[ChapterResponse]
    total: int
    novel_id: int
