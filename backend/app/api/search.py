from typing import Optional, List
from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models import Novel, Chapter
from app.schemas import NovelResponse, ChapterResponse

router = APIRouter()


@router.get("")
async def search(
    keyword: str = Query(..., min_length=1),
    type: str = Query("title", regex="^(title|author|content)$"),
    session: AsyncSession = Depends(get_session)
):
    """搜索"""
    results = []

    if type in ["title", "author"]:
        # 搜索小说标题或作者
        query = select(Novel)
        if type == "title":
            query = query.where(Novel.title.contains(keyword))
        else:
            query = query.where(Novel.author.contains(keyword))

        result = await session.execute(query.limit(20))
        novels = result.scalars().all()

        results = [
            {
                "type": "novel",
                "id": n.id,
                "title": n.title,
                "author": n.author,
                "source_site": n.source_site
            }
            for n in novels
        ]

    elif type == "content":
        # 搜索章节内容
        query = select(Chapter).where(Chapter.content.contains(keyword)).limit(20)
        result = await session.execute(query)
        chapters = result.scalars().all()

        # 获取关联的小说信息
        results = []
        for c in chapters:
            novel = await session.get(Novel, c.novel_id)
            results.append({
                "type": "chapter",
                "id": c.id,
                "title": c.title,
                "novel_id": c.novel_id,
                "novel_title": novel.title if novel else None,
                "content_preview": c.content[:100] if c.content else None
            })

    return {"keyword": keyword, "type": type, "results": results}
