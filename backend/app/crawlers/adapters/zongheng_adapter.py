"""
纵横中文网适配器

纵横中文网的章节列表需要通过阅读器页面动态加载获取。
书籍详情页只显示基本信息，完整目录需要访问阅读器页面。
"""
import re
import asyncio
from typing import Optional, Dict, Any, List
from urllib.parse import urljoin

from app.crawlers.base import BaseSiteAdapter, NovelInfo, ChapterInfo, ChapterContent
from app.crawlers.anti_crawler import AntiCrawlerHandler


class ZonghengAdapter(BaseSiteAdapter):
    """纵横中文网适配器"""

    def __init__(self, rule: Optional[Dict[str, Any]] = None):
        super().__init__(rule)
        self.handler = AntiCrawlerHandler()
        self._playwright = None
        self._browser = None

    async def _ensure_browser(self):
        """确保Playwright浏览器已启动"""
        if self._playwright is None:
            from playwright.async_api import async_playwright
            self._playwright = await async_playwright().start()
        if self._browser is None:
            self._browser = await self._playwright.chromium.launch(headless=True)

    async def close(self):
        """关闭资源"""
        await self.handler.close()
        if self._browser:
            await self._browser.close()
        if self._playwright:
            await self._playwright.stop()

    def _extract_book_id(self, url: str) -> Optional[str]:
        """从URL中提取书籍ID"""
        # URL格式: https://www.zongheng.com/book/1324769.html
        match = re.search(r'/book/(\d+)', url)
        if match:
            return match.group(1)
        return None

    def _extract_chapter_id(self, url: str) -> Optional[str]:
        """从URL中提取章节ID"""
        # URL格式: https://read.zongheng.com/chapter/1324769/77229326.html
        match = re.search(r'/chapter/\d+/(\d+)', url)
        if match:
            return match.group(1)
        return None

    async def get_novel_info(self, url: str) -> NovelInfo:
        """获取小说基本信息"""
        html = await self.handler.fetch(url)

        # 从meta标签提取信息
        title = self._extract_meta(html, 'og:novel:book_name')
        author = self._extract_meta(html, 'og:novel:author')
        cover_url = self._extract_meta(html, 'og:image')
        description = self._extract_meta(html, 'og:description')
        status = self._extract_meta(html, 'og:novel:status')

        # 获取最新章节URL作为阅读入口
        first_chapter_url = self._get_first_chapter_url(html, url)

        return NovelInfo(
            title=title or "未知书名",
            author=author,
            cover_url=cover_url,
            description=description,
            status=status or "连载中",
            first_chapter_url=first_chapter_url
        )

    def _extract_meta(self, html: str, property_name: str) -> Optional[str]:
        """从meta标签提取内容"""
        pattern = rf'<meta\s+property="{property_name}"\s+content="([^"]*)"'
        match = re.search(pattern, html)
        if match:
            return match.group(1)
        return None

    def _get_first_chapter_url(self, html: str, base_url: str) -> Optional[str]:
        """获取第一章URL"""
        # 查找"开始阅读"链接
        match = re.search(r'<a[^>]*href="(https://read\.zongheng\.com/chapter/\d+/\d+\.html)"[^>]*>[^<]*开始阅读[^<]*</a>', html)
        if match:
            return match.group(1)

        # 或者查找read.zongheng.com的chapter链接
        match = re.search(r'https://read\.zongheng\.com/chapter/\d+/\d+\.html', html)
        if match:
            return match.group(0)

        return None

    async def get_chapter_list(self, url: str) -> List[ChapterInfo]:
        """获取章节列表

        纵横中文网的章节列表在阅读器页面动态加载，
        需要使用JS渲染获取完整目录。
        """
        # 先获取阅读入口URL
        html = await self.handler.fetch(url)
        reader_url = self._get_first_chapter_url(html, url)

        if not reader_url:
            book_id = self._extract_book_id(url)
            if book_id:
                match = re.search(r'https://read\.zongheng\.com/chapter/\d+/(\d+)\.html', html)
                if match:
                    chapter_id = match.group(1)
                    reader_url = f"https://read.zongheng.com/chapter/{book_id}/{chapter_id}.html"

        if not reader_url:
            return []

        # 确保浏览器已启动
        await self._ensure_browser()

        page = await self._browser.new_page()

        try:
            # 设置User-Agent
            await page.set_extra_http_headers({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            })

            await page.goto(reader_url, wait_until="networkidle", timeout=30000)
            await asyncio.sleep(2)  # 等待内容加载

            # 获取所有链接
            links = await page.query_selector_all('a')

            chapters = []
            seen_ids = set()

            for link in links:
                href = await link.get_attribute('href') or ''
                text = await link.inner_text()

                # 提取章节ID - 必须是/chapter/格式
                match = re.search(r'/chapter/\d+/(\d+)\.html', href)
                if match:
                    chapter_id = match.group(1)
                    # 过滤掉非章节链接（如"下一章"、目录等）
                    # 真正的章节标题通常包含"第X章"
                    if '下一章' in text or '上一章' in text or '目录' in text:
                        continue

                    if chapter_id not in seen_ids:
                        seen_ids.add(chapter_id)

                        # 构建完整URL
                        book_id = self._extract_book_id(url)
                        chapter_url = f"https://read.zongheng.com/chapter/{book_id}/{chapter_id}.html"

                        # 提取章节序号
                        index_match = re.search(r'第(\d+)章', text)
                        index = int(index_match.group(1)) if index_match else len(chapters) + 1

                        chapters.append(ChapterInfo(
                            index=index,
                            title=text.strip(),
                            url=chapter_url
                        ))

            # 按章节序号排序
            chapters.sort(key=lambda c: c.index)
            return chapters

        finally:
            await page.close()

    async def get_chapter_content(self, url: str) -> ChapterContent:
        """获取章节内容"""
        # 确保浏览器已启动
        await self._ensure_browser()

        page = await self._browser.new_page()

        try:
            # 设置User-Agent
            await page.set_extra_http_headers({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            })

            await page.goto(url, wait_until="networkidle", timeout=30000)
            await asyncio.sleep(2)  # 等待内容加载

            # 获取标题
            title_elem = await page.query_selector('.title, .chapter-title, .reader_chapter_title')
            title = await title_elem.inner_text() if title_elem else "未知章节"

            # 获取内容
            content_elem = await page.query_selector('.content, .chapter-content, .reader_chapter_content')
            content = await content_elem.inner_text() if content_elem else ""

            # 清理内容
            content = content.strip()

            return ChapterContent(title=title.strip(), content=content)

        finally:
            await page.close()
