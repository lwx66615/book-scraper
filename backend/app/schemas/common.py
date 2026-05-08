from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class PaginatedResponse(BaseModel):
    total: int
    page: int
    page_size: int
    total_pages: int


class MessageResponse(BaseModel):
    message: str
    success: bool = True
