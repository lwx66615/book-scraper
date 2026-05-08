import pytest
from app.crawlers.anti_crawler import AntiCrawlerHandler


@pytest.mark.asyncio
async def test_get_random_ua():
    handler = AntiCrawlerHandler()
    ua = handler.get_random_ua()
    assert ua is not None
    assert "Mozilla" in ua


@pytest.mark.asyncio
async def test_detect_captcha():
    handler = AntiCrawlerHandler()

    html_with_captcha = "<html><body>请输入验证码继续访问</body></html>"
    assert handler.detect_captcha(html_with_captcha) is True

    html_without_captcha = "<html><body>小说内容</body></html>"
    assert handler.detect_captcha(html_without_captcha) is False
