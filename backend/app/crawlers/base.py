from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from bs4 import BeautifulSoup


@dataclass
class NovelInfo:
    """小说基本信息"""
    title: str
    author: Optional[str] = None
    cover_url: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    first_chapter_url: Optional[str] = None  # 用于获取章节列表的入口


@dataclass
class ChapterInfo:
    """章节信息"""
    index: int
    title: str
    url: str


@dataclass
class ChapterContent:
    """章节内容"""
    title: str
    content: str


class BaseSiteAdapter(ABC):
    """网站适配器基类"""

    def __init__(self, rule: Optional[Dict[str, Any]] = None):
        self.rule = rule or {}
        self.selectors = rule.get("selectors", {}) if rule else {}

    @abstractmethod
    async def get_novel_info(self, url: str) -> NovelInfo:
        """获取小说基本信息"""
        pass

    @abstractmethod
    async def get_chapter_list(self, url: str) -> List[ChapterInfo]:
        """获取章节列表"""
        pass

    @abstractmethod
    async def get_chapter_content(self, url: str) -> ChapterContent:
        """获取章节内容"""
        pass

    def parse_html(self, html: str) -> BeautifulSoup:
        """解析HTML"""
        return BeautifulSoup(html, "lxml")

    def clean_content(self, content: str) -> str:
        """清理内容（去除广告等）"""
        # 移除常见广告关键词
        ad_keywords = ["请记住本站域名", "最快更新", "无弹窗", "广告"]
        for keyword in ad_keywords:
            content = content.replace(keyword, "")
        return content.strip()
