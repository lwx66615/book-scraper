import random
import asyncio
from typing import Optional, List, Dict
import aiohttp
from playwright.async_api import async_playwright, Browser, Page

from app.config import settings


class AntiCrawlerHandler:
    """反爬处理器"""

    # User-Agent池
    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    ]

    def __init__(self):
        self.session: Optional[aiohttp.ClientSession] = None
        self.browser: Optional[Browser] = None
        self.proxy_index = 0
        self.cookie_jar: Dict[str, Dict[str, str]] = {}  # 按域名存储cookie

    async def init_session(self):
        """初始化HTTP会话"""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()

    async def close(self):
        """关闭资源"""
        if self.session and not self.session.closed:
            await self.session.close()
        if self.browser:
            await self.browser.close()

    def get_random_ua(self) -> str:
        """获取随机User-Agent"""
        return random.choice(self.USER_AGENTS)

    def get_proxy(self) -> Optional[str]:
        """获取代理"""
        if not settings.proxy_list:
            return None
        proxy = settings.proxy_list[self.proxy_index]
        self.proxy_index = (self.proxy_index + 1) % len(settings.proxy_list)
        return proxy

    async def delay(self):
        """随机延迟"""
        delay = random.uniform(settings.request_delay_min, settings.request_delay_max)
        await asyncio.sleep(delay)

    async def fetch(
        self,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        use_proxy: bool = False,
        require_js: bool = False
    ) -> str:
        """
        获取页面内容

        Args:
            url: 目标URL
            headers: 自定义请求头
            use_proxy: 是否使用代理
            require_js: 是否需要JS渲染

        Returns:
            页面HTML内容
        """
        await self.delay()

        if require_js:
            return await self._fetch_with_js(url, headers)

        return await self._fetch_with_http(url, headers, use_proxy)

    async def _fetch_with_http(
        self,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        use_proxy: bool = False
    ) -> str:
        """使用aiohttp获取页面"""
        await self.init_session()

        default_headers = {
            "User-Agent": self.get_random_ua(),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        }
        if headers:
            default_headers.update(headers)

        # 添加存储的cookie
        domain = self._extract_domain(url)
        if domain in self.cookie_jar:
            cookie_str = "; ".join(f"{k}={v}" for k, v in self.cookie_jar[domain].items())
            default_headers["Cookie"] = cookie_str

        proxy = self.get_proxy() if use_proxy else None

        for attempt in range(settings.max_retries):
            try:
                async with self.session.get(
                    url,
                    headers=default_headers,
                    proxy=proxy,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status == 200:
                        html = await response.text()

                        # 保存cookie
                        cookies = response.cookies
                        if cookies:
                            if domain not in self.cookie_jar:
                                self.cookie_jar[domain] = {}
                            for name, cookie in cookies.items():
                                self.cookie_jar[domain][name] = cookie.value

                        return html
                    elif response.status == 403:
                        raise Exception(f"访问被拒绝(403)，可能需要验证码或更换IP")
                    else:
                        raise Exception(f"HTTP错误: {response.status}")

            except aiohttp.ClientError as e:
                if attempt == settings.max_retries - 1:
                    raise Exception(f"请求失败: {str(e)}")
                await asyncio.sleep(2 ** attempt)  # 指数退避

        raise Exception("请求失败")

    async def _fetch_with_js(
        self,
        url: str,
        headers: Optional[Dict[str, str]] = None
    ) -> str:
        """使用Playwright获取JS渲染页面"""
        if self.browser is None:
            playwright = await async_playwright().start()
            self.browser = await playwright.chromium.launch(headless=True)

        page = await self.browser.new_page()

        try:
            if headers:
                await page.set_extra_http_headers(headers)

            await page.set_extra_http_headers({
                "User-Agent": self.get_random_ua()
            })

            await page.goto(url, wait_until="networkidle", timeout=30000)
            html = await page.content()

            return html

        finally:
            await page.close()

    def _extract_domain(self, url: str) -> str:
        """提取域名"""
        from urllib.parse import urlparse
        parsed = urlparse(url)
        return parsed.netloc

    def detect_captcha(self, html: str) -> bool:
        """检测是否有验证码"""
        captcha_keywords = ["验证码", "captcha", "请输入验证码", "安全验证"]
        html_lower = html.lower()
        return any(keyword in html_lower for keyword in captcha_keywords)
