from typing import Dict, Any, Optional

from app.crawlers.base import BaseSiteAdapter, NovelInfo, ChapterInfo, ChapterContent
from app.crawlers.anti_crawler import AntiCrawlerHandler


class ExampleSiteAdapter(BaseSiteAdapter):
    """
    示例网站适配器

    这是一个模板，展示如何为特定网站创建适配器。
    实际使用时，需要根据目标网站的具体结构进行修改。
    """

    # 网站特定的选择器配置
    SITE_SELECTORS = {
        "book_title": "h1.book-name",
        "book_author": ".book-info .author",
        "chapter_list": ".chapter-list a",
        "chapter_title": "h1.chapter-title",
        "chapter_content": ".chapter-content",
    }

    def __init__(self, rule: Optional[Dict[str, Any]] = None):
        super().__init__(rule)
        self.handler = AntiCrawlerHandler()
        # 合并网站特定选择器和规则中的选择器
        self.selectors = {**self.SITE_SELECTORS, **self.selectors}

    async def close(self):
        await self.handler.close()

    async def get_novel_info(self, url: str) -> NovelInfo:
        """获取小说基本信息"""
        html = await self.handler.fetch(url)
        soup = self.parse_html(html)

        title_elem = soup.select_one(self.selectors["book_title"])
        author_elem = soup.select_one(self.selectors["book_author"])

        return NovelInfo(
            title=title_elem.get_text(strip=True) if title_elem else "未知",
            author=author_elem.get_text(strip=True) if author_elem else None,
        )

    async def get_chapter_list(self, url: str) -> list[ChapterInfo]:
        """获取章节列表"""
        html = await self.handler.fetch(url)
        soup = self.parse_html(html)

        chapters = []
        links = soup.select(self.selectors["chapter_list"])

        for index, link in enumerate(links, 1):
            from urllib.parse import urljoin
            chapter_url = urljoin(url, link.get("href", ""))
            title = link.get_text(strip=True)

            chapters.append(ChapterInfo(
                index=index,
                title=title,
                url=chapter_url
            ))

        return chapters

    async def get_chapter_content(self, url: str) -> ChapterContent:
        """获取章节内容"""
        html = await self.handler.fetch(url)
        soup = self.parse_html(html)

        title_elem = soup.select_one(self.selectors["chapter_title"])
        content_elem = soup.select_one(self.selectors["chapter_content"])

        title = title_elem.get_text(strip=True) if title_elem else "未知章节"
        content = content_elem.get_text(separator="\n", strip=True) if content_elem else ""
        content = self.clean_content(content)

        return ChapterContent(title=title, content=content)
