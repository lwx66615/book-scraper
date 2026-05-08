import re
from typing import List, Optional, Dict, Any
from urllib.parse import urljoin, urlparse

from app.crawlers.base import BaseSiteAdapter, NovelInfo, ChapterInfo, ChapterContent
from app.crawlers.anti_crawler import AntiCrawlerHandler


class GenericSiteAdapter(BaseSiteAdapter):
    """通用网站适配器"""

    # 常见选择器模式
    COMMON_SELECTORS = {
        "book_title": ["h1", "h2.title", ".book-title", "#info h1", "h1.title"],
        "book_author": [".author", "#info p", ".book-author", "meta[name=author]"],
        "chapter_list": ["#list a", "#chapters a", ".chapter-list a", ".list a", "#chapter-list a"],
        "chapter_content": ["#content", ".content", ".chapter-content", "#chaptercontent", ".text-content"],
        "chapter_title": ["h1", ".title", "h2"],
    }

    def __init__(self, rule: Optional[Dict[str, Any]] = None):
        super().__init__(rule)
        self.handler = AntiCrawlerHandler()

    async def close(self):
        await self.handler.close()

    async def get_novel_info(self, url: str) -> NovelInfo:
        """获取小说基本信息"""
        html = await self.handler.fetch(url, require_js=self.rule.get("requires_js", False))
        soup = self.parse_html(html)

        title = self._extract_with_fallback(soup, "book_title")
        author = self._extract_with_fallback(soup, "book_author")

        # 尝试获取封面
        cover_url = None
        cover_img = soup.select_one("img.cover, .book-cover img, #fmimg img")
        if cover_img and cover_img.get("src"):
            cover_url = urljoin(url, cover_img["src"])

        # 尝试获取简介
        description = None
        desc_elem = soup.select_one("#intro, .intro, .description, .book-intro")
        if desc_elem:
            description = desc_elem.get_text(strip=True)

        # 尝试获取状态
        status = "连载中"
        status_text = soup.get_text()
        if "完结" in status_text or "完本" in status_text:
            status = "已完结"

        return NovelInfo(
            title=title or "未知书名",
            author=author,
            cover_url=cover_url,
            description=description,
            status=status
        )

    async def get_chapter_list(self, url: str) -> List[ChapterInfo]:
        """获取章节列表"""
        html = await self.handler.fetch(url, require_js=self.rule.get("requires_js", False))
        soup = self.parse_html(html)

        chapters = []
        chapter_links = self._find_chapter_links(soup)

        for index, link in enumerate(chapter_links, 1):
            href = link.get("href")
            if not href:
                continue

            chapter_url = urljoin(url, href)
            title = link.get_text(strip=True)

            chapters.append(ChapterInfo(
                index=index,
                title=title or f"第{index}章",
                url=chapter_url
            ))

        return chapters

    async def get_chapter_content(self, url: str) -> ChapterContent:
        """获取章节内容"""
        html = await self.handler.fetch(url, require_js=self.rule.get("requires_js", False))
        soup = self.parse_html(html)

        title = self._extract_with_fallback(soup, "chapter_title") or "未知章节"
        content = self._extract_content(soup)

        # 清理内容
        content = self.clean_content(content)

        return ChapterContent(title=title, content=content)

    def _extract_with_fallback(self, soup, selector_type: str) -> Optional[str]:
        """使用多个选择器尝试提取"""
        selectors = self.selectors.get(selector_type) if self.selectors else None

        if selectors:
            # 使用配置的选择器
            if isinstance(selectors, str):
                selectors = [selectors]
            for sel in selectors:
                elem = soup.select_one(sel)
                if elem:
                    return elem.get_text(strip=True)

        # 使用常见选择器
        for sel in self.COMMON_SELECTORS.get(selector_type, []):
            elem = soup.select_one(sel)
            if elem:
                text = elem.get_text(strip=True)
                if text:
                    return text

        return None

    def _find_chapter_links(self, soup) -> List:
        """查找章节链接"""
        # 先尝试配置的选择器
        if self.selectors and "chapter_list" in self.selectors:
            sel = self.selectors["chapter_list"]
            links = soup.select(sel)
            if links:
                return links

        # 使用常见选择器
        for sel in self.COMMON_SELECTORS["chapter_list"]:
            links = soup.select(sel)
            if links:
                return links

        # 尝试查找所有包含章节特征的链接
        all_links = soup.select("a")
        chapter_links = []
        for link in all_links:
            text = link.get_text(strip=True)
            href = link.get("href", "")
            # 匹配常见章节标题模式
            if re.search(r"第[零一二三四五六七八九十百千万\d]+[章节回]", text) or \
               re.search(r"chapter\s*\d+", text, re.I) or \
               re.search(r"/\d+\.html?$", href):
                chapter_links.append(link)

        return chapter_links

    def _extract_content(self, soup) -> str:
        """提取章节内容"""
        # 先尝试配置的选择器
        if self.selectors and "chapter_content" in self.selectors:
            sel = self.selectors["chapter_content"]
            elem = soup.select_one(sel)
            if elem:
                return elem.get_text(separator="\n", strip=True)

        # 使用常见选择器
        for sel in self.COMMON_SELECTORS["chapter_content"]:
            elem = soup.select_one(sel)
            if elem:
                text = elem.get_text(separator="\n", strip=True)
                if len(text) > 100:  # 内容应该足够长
                    return text

        # 尝试查找最长的文本块
        paragraphs = soup.find_all("p")
        if paragraphs:
            content = "\n".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))
            if len(content) > 100:
                return content

        return ""
