from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.services.novel_service import NovelService
from app.schemas import (
    NovelResponse, NovelListResponse, NovelDetailResponse,
    NovelUpdate, ChapterListResponse, ChapterContentResponse,
    MessageResponse
)

router = APIRouter()


def get_novel_service(session: AsyncSession = Depends(get_session)) -> NovelService:
    return NovelService(session)


@router.get("", response_model=NovelListResponse)
async def get_novels(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    tag: Optional[str] = None,
    keyword: Optional[str] = None,
    service: NovelService = Depends(get_novel_service)
):
    """获取小说列表"""
    novels, total = await service.get_list(page, page_size, tag, keyword)

    return NovelListResponse(
        items=[NovelResponse.model_validate(n) for n in novels],
        total=total,
        page=page,
        page_size=page_size
    )


@router.get("/{novel_id}", response_model=NovelDetailResponse)
async def get_novel(
    novel_id: int,
    service: NovelService = Depends(get_novel_service)
):
    """获取小说详情"""
    novel = await service.get_by_id(novel_id)
    if not novel:
        raise HTTPException(status_code=404, detail="小说不存在")

    progress = await service.get_reading_progress(novel_id)

    # 构建响应数据
    response_data = {
        "id": novel.id,
        "title": novel.title,
        "author": novel.author,
        "source_url": novel.source_url,
        "source_site": novel.source_site,
        "cover_url": novel.cover_url,
        "description": novel.description,
        "status": novel.status,
        "tags": novel.tags,
        "total_chapters": novel.total_chapters,
        "created_at": novel.created_at,
        "updated_at": novel.updated_at,
        "chapters_count": len(novel.chapters),
        "reading_progress": {
            "last_chapter_id": progress.last_chapter_id if progress else None,
            "last_position": progress.last_position if progress else 0
        }
    }

    return NovelDetailResponse(**response_data)


@router.delete("/{novel_id}", response_model=MessageResponse)
async def delete_novel(
    novel_id: int,
    service: NovelService = Depends(get_novel_service)
):
    """删除小说"""
    success = await service.delete(novel_id)
    if not success:
        raise HTTPException(status_code=404, detail="小说不存在")

    return MessageResponse(message="删除成功")


@router.get("/{novel_id}/chapters", response_model=ChapterListResponse)
async def get_novel_chapters(
    novel_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    service: NovelService = Depends(get_novel_service)
):
    """获取小说章节列表"""
    novel = await service.get_by_id(novel_id)
    if not novel:
        raise HTTPException(status_code=404, detail="小说不存在")

    chapters, total = await service.get_chapters(novel_id, page, page_size)

    from app.schemas.chapter import ChapterResponse
    return ChapterListResponse(
        items=[ChapterResponse.model_validate(c) for c in chapters],
        total=total,
        novel_id=novel_id
    )


@router.get("/chapters/{chapter_id}", response_model=ChapterContentResponse)
async def get_chapter(
    chapter_id: int,
    service: NovelService = Depends(get_novel_service)
):
    """获取章节内容"""
    chapter = await service.get_chapter(chapter_id)
    if not chapter:
        raise HTTPException(status_code=404, detail="章节不存在")

    return ChapterContentResponse.model_validate(chapter)
