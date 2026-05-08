import pytest
from app.crawlers.generic_adapter import GenericSiteAdapter


@pytest.mark.asyncio
async def test_adapter_init():
    adapter = GenericSiteAdapter()
    assert adapter.handler is not None
    await adapter.close()


@pytest.mark.asyncio
async def test_extract_with_fallback():
    from bs4 import BeautifulSoup

    adapter = GenericSiteAdapter()
    html = "<html><body><h1 class='title'>测试书名</h1></body></html>"
    soup = adapter.parse_html(html)

    title = adapter._extract_with_fallback(soup, "book_title")
    assert title == "测试书名"

    await adapter.close()


@pytest.mark.asyncio
async def test_find_chapter_links():
    from bs4 import BeautifulSoup

    adapter = GenericSiteAdapter()
    html = """
    <html><body>
        <div id="list">
            <a href="/chapter/1">第一章 开始</a>
            <a href="/chapter/2">第二章 继续</a>
        </div>
    </body></html>
    """
    soup = adapter.parse_html(html)

    links = adapter._find_chapter_links(soup)
    assert len(links) == 2
    assert links[0].get_text(strip=True) == "第一章 开始"

    await adapter.close()


@pytest.mark.asyncio
async def test_clean_content():
    adapter = GenericSiteAdapter()

    dirty_content = "这是正文内容。请记住本站域名：xxx.com最快更新无弹窗"
    clean = adapter.clean_content(dirty_content)

    assert "请记住本站域名" not in clean
    assert "最快更新" not in clean
    assert "正文内容" in clean
