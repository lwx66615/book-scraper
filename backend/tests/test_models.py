import pytest
from app.models import Novel, Chapter, SiteRule, DownloadTask, ReadingProgress


@pytest.mark.asyncio
async def test_create_novel(db_session):
    novel = Novel(
        title="测试小说",
        author="测试作者",
        source_url="https://example.com/novel/1",
        source_site="example.com"
    )
    db_session.add(novel)
    await db_session.commit()

    assert novel.id is not None
    assert novel.title == "测试小说"
    assert novel.status == "连载中"


@pytest.mark.asyncio
async def test_create_chapter(db_session):
    novel = Novel(title="测试小说", source_url="https://example.com/novel/1")
    db_session.add(novel)
    await db_session.commit()

    chapter = Chapter(
        novel_id=novel.id,
        chapter_index=1,
        title="第一章",
        content="这是第一章的内容",
        source_url="https://example.com/novel/1/1"
    )
    db_session.add(chapter)
    await db_session.commit()

    assert chapter.id is not None
    assert chapter.novel_id == novel.id


@pytest.mark.asyncio
async def test_create_site_rule(db_session):
    rule = SiteRule(
        site_name="测试网站",
        site_url="https://example.com",
        rule_type="specific",
        selectors={
            "book_title": "h1.title",
            "book_author": ".author",
            "chapter_list": "#chapter-list a",
            "chapter_content": "#content"
        }
    )
    db_session.add(rule)
    await db_session.commit()

    assert rule.id is not None
    assert rule.is_active is True


@pytest.mark.asyncio
async def test_create_download_task(db_session):
    novel = Novel(title="测试小说", source_url="https://example.com/novel/1")
    db_session.add(novel)
    await db_session.commit()

    task = DownloadTask(novel_id=novel.id, total_chapters=100)
    db_session.add(task)
    await db_session.commit()

    assert task.id is not None
    assert task.status == "pending"


@pytest.mark.asyncio
async def test_create_reading_progress(db_session):
    novel = Novel(title="测试小说", source_url="https://example.com/novel/1")
    db_session.add(novel)
    await db_session.commit()

    progress = ReadingProgress(novel_id=novel.id, last_chapter_id=1)
    db_session.add(progress)
    await db_session.commit()

    assert progress.id is not None
