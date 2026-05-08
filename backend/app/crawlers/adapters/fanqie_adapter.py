"""
番茄小说适配器

番茄小说使用了字体加密技术，内容中的汉字被替换成Unicode私有区域字符。
需要从 __INITIAL_STATE__ 中提取数据。
"""
import re
import json
from typing import Optional, Dict, Any, List
from urllib.parse import urljoin

from app.crawlers.base import BaseSiteAdapter, NovelInfo, ChapterInfo, ChapterContent
from app.crawlers.anti_crawler import AntiCrawlerHandler


class FanqieAdapter(BaseSiteAdapter):
    """番茄小说适配器"""

    def __init__(self, rule: Optional[Dict[str, Any]] = None):
        super().__init__(rule)
        self.handler = AntiCrawlerHandler()

    async def close(self):
        await self.handler.close()

    def _extract_initial_state(self, html: str) -> Optional[dict]:
        """从页面中提取 __INITIAL_STATE__ 数据"""
        match = re.search(r'__INITIAL_STATE__=({.*?});', html, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError:
                return None
        return None

    async def get_novel_info(self, url: str) -> NovelInfo:
        """获取小说基本信息"""
        html = await self.handler.fetch(url)
        state = self._extract_initial_state(html)

        if not state:
            # 尝试从阅读页获取书籍ID，然后访问书籍详情页
            return NovelInfo(title="未知书名")

        chapter_data = state.get('reader', {}).get('chapterData', {})

        return NovelInfo(
            title=chapter_data.get('bookName', '未知书名'),
            author=chapter_data.get('author'),
            description=None,  # 需要从书籍详情页获取
            status='连载中'  # 需要从书籍详情页获取
        )

    async def get_chapter_list(self, url: str) -> List[ChapterInfo]:
        """获取章节列表

        注意：番茄小说的阅读页URL是单个章节，需要从书籍详情页获取完整目录
        这里返回当前章节作为示例
        """
        html = await self.handler.fetch(url)
        state = self._extract_initial_state(html)

        if not state:
            return []

        chapter_data = state.get('reader', {}).get('chapterData', {})

        # 从阅读页只能获取当前章节信息
        # 实际使用时需要访问书籍详情页获取完整目录
        chapters = []

        current_chapter = ChapterInfo(
            index=int(chapter_data.get('order', 1)),
            title=chapter_data.get('title', '未知章节'),
            url=url
        )
        chapters.append(current_chapter)

        return chapters

    async def get_chapter_content(self, url: str) -> ChapterContent:
        """获取章节内容

        注意：番茄小说使用字体加密，返回的内容可能是乱码
        需要额外的字体映射才能正确解码
        """
        html = await self.handler.fetch(url)
        state = self._extract_initial_state(html)

        if not state:
            return ChapterContent(title="获取失败", content="")

        chapter_data = state.get('reader', {}).get('chapterData', {})

        title = chapter_data.get('title', '未知章节')

        # 获取加密的内容
        content_html = chapter_data.get('content', '')
        # 移除HTML标签
        content = re.sub(r'<[^>]+>', '', content_html)
        # 移除多余空白
        content = re.sub(r'\s+', '', content)

        # 注意：这里的内容是字体加密的，显示为乱码
        # 需要字体映射才能正确显示

        return ChapterContent(
            title=title,
            content=f"[字体加密内容，需要解码]\n\n原始内容:\n{content[:500]}..."
        )

    def get_book_id_from_url(self, url: str) -> Optional[str]:
        """从URL中提取书籍ID"""
        # 阅读页URL格式: https://fanqienovel.com/reader/{itemId}
        match = re.search(r'/reader/(\d+)', url)
        if match:
            return match.group(1)
        return None
