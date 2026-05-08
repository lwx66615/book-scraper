from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel


class SelectorsConfig(BaseModel):
    book_title: Optional[str] = None
    book_author: Optional[str] = None
    chapter_list: Optional[str] = None
    chapter_title: Optional[str] = None
    chapter_content: Optional[str] = None


class SiteRuleBase(BaseModel):
    site_name: str
    site_url: str
    is_active: bool = True
    rule_type: str = "generic"
    selectors: Optional[Dict[str, Any]] = None
    headers: Optional[Dict[str, str]] = None
    requires_js: bool = False


class SiteRuleCreate(SiteRuleBase):
    pass


class SiteRuleUpdate(BaseModel):
    site_name: Optional[str] = None
    site_url: Optional[str] = None
    is_active: Optional[bool] = None
    rule_type: Optional[str] = None
    selectors: Optional[Dict[str, Any]] = None
    headers: Optional[Dict[str, str]] = None
    requires_js: Optional[bool] = None


class SiteRuleResponse(SiteRuleBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class SiteRuleListResponse(BaseModel):
    items: List[SiteRuleResponse]
    total: int


class RuleTestRequest(BaseModel):
    rule_id: Optional[int] = None
    test_url: str


class RuleTestResult(BaseModel):
    success: bool
    message: str
    extracted_data: Optional[Dict[str, Any]] = None
