from app.schemas.common import PaginatedResponse, MessageResponse
from app.schemas.novel import (
    NovelCreate, NovelUpdate, NovelResponse,
    NovelListResponse, NovelDetailResponse
)
from app.schemas.chapter import (
    ChapterCreate, ChapterResponse,
    ChapterContentResponse, ChapterListResponse
)
from app.schemas.site_rule import (
    SiteRuleCreate, SiteRuleUpdate, SiteRuleResponse,
    SiteRuleListResponse, RuleTestRequest, RuleTestResult
)
from app.schemas.download_task import (
    DownloadStartRequest, DownloadTaskResponse,
    DownloadTaskListResponse, DownloadProgressResponse
)

__all__ = [
    "PaginatedResponse", "MessageResponse",
    "NovelCreate", "NovelUpdate", "NovelResponse",
    "NovelListResponse", "NovelDetailResponse",
    "ChapterCreate", "ChapterResponse",
    "ChapterContentResponse", "ChapterListResponse",
    "SiteRuleCreate", "SiteRuleUpdate", "SiteRuleResponse",
    "SiteRuleListResponse", "RuleTestRequest", "RuleTestResult",
    "DownloadStartRequest", "DownloadTaskResponse",
    "DownloadTaskListResponse", "DownloadProgressResponse",
]
