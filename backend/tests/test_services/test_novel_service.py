import pytest
from app.services.novel_service import NovelService
from app.schemas import NovelCreate, NovelUpdate


@pytest.mark.asyncio
async def test_create_novel(db_session):
    service = NovelService(db_session)
    novel_data = NovelCreate(
        title="测试小说",
        author="测试作者",
        source_url="https://example.com/novel/1"
    )

    novel = await service.create(novel_data)

    assert novel.id is not None
    assert novel.title == "测试小说"


@pytest.mark.asyncio
async def test_get_novel_by_id(db_session):
    service = NovelService(db_session)
    novel_data = NovelCreate(
        title="测试小说",
        source_url="https://example.com/novel/1"
    )
    created = await service.create(novel_data)

    novel = await service.get_by_id(created.id)

    assert novel is not None
    assert novel.title == "测试小说"


@pytest.mark.asyncio
async def test_get_novel_list(db_session):
    service = NovelService(db_session)

    # 创建多个小说
    for i in range(3):
        await service.create(NovelCreate(
            title=f"小说{i}",
            source_url=f"https://example.com/novel/{i}"
        ))

    novels, total = await service.get_list(page=1, page_size=10)

    assert total == 3
    assert len(novels) == 3


@pytest.mark.asyncio
async def test_update_novel(db_session):
    service = NovelService(db_session)
    novel = await service.create(NovelCreate(
        title="原标题",
        source_url="https://example.com/novel/1"
    ))

    updated = await service.update(novel.id, NovelUpdate(title="新标题"))

    assert updated.title == "新标题"


@pytest.mark.asyncio
async def test_delete_novel(db_session):
    service = NovelService(db_session)
    novel = await service.create(NovelCreate(
        title="待删除",
        source_url="https://example.com/novel/1"
    ))

    result = await service.delete(novel.id)

    assert result is True

    deleted = await service.get_by_id(novel.id)
    assert deleted is None
