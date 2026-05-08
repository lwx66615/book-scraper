"""爬虫模块"""
from app.crawlers.base import BaseSiteAdapter, NovelInfo, ChapterInfo, ChapterContent
from app.crawlers.anti_crawler import AntiCrawlerHandler
from app.crawlers.generic_adapter import GenericSiteAdapter

__all__ = [
    "BaseSiteAdapter",
    "NovelInfo",
    "ChapterInfo",
    "ChapterContent",
    "AntiCrawlerHandler",
    "GenericSiteAdapter",
]