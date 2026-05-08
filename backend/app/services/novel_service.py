from typing import Optional, List
from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import Novel, Chapter, ReadingProgress
from app.schemas import NovelCreate, NovelUpdate


class NovelService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, novel_data: NovelCreate) -> Novel:
        """创建小说"""
        novel = Novel(**novel_data.model_dump())
        self.session.add(novel)
        await self.session.commit()
        await self.session.refresh(novel)
        return novel

    async def get_by_id(self, novel_id: int) -> Optional[Novel]:
        """根据ID获取小说"""
        result = await self.session.execute(
            select(Novel).options(selectinload(Novel.chapters)).where(Novel.id == novel_id)
        )
        return result.scalar_one_or_none()

    async def get_list(
        self,
        page: int = 1,
        page_size: int = 20,
        tag: Optional[str] = None,
        keyword: Optional[str] = None
    ) -> tuple[List[Novel], int]:
        """获取小说列表"""
        query = select(Novel)

        # 标签筛选
        if tag:
            query = query.where(Novel.tags.contains(tag))

        # 关键词搜索
        if keyword:
            query = query.where(
                or_(
                    Novel.title.contains(keyword),
                    Novel.author.contains(keyword)
                )
            )

        # 统计总数
        count_query = select(func.count()).select_from(query.subquery())
        total = await self.session.scalar(count_query)

        # 分页
        query = query.order_by(Novel.updated_at.desc())
        query = query.offset((page - 1) * page_size).limit(page_size)

        result = await self.session.execute(query)
        novels = list(result.scalars().all())

        return novels, total

    async def update(self, novel_id: int, novel_data: NovelUpdate) -> Optional[Novel]:
        """更新小说"""
        novel = await self.get_by_id(novel_id)
        if not novel:
            return None

        update_data = novel_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(novel, key, value)

        await self.session.commit()
        await self.session.refresh(novel)
        return novel

    async def delete(self, novel_id: int) -> bool:
        """删除小说"""
        novel = await self.get_by_id(novel_id)
        if not novel:
            return False

        await self.session.delete(novel)
        await self.session.commit()
        return True

    async def get_chapters(self, novel_id: int, page: int = 1, page_size: int = 50) -> tuple[List[Chapter], int]:
        """获取小说章节列表"""
        count_query = select(func.count()).where(Chapter.novel_id == novel_id)
        total = await self.session.scalar(count_query)

        query = select(Chapter).where(Chapter.novel_id == novel_id)
        query = query.order_by(Chapter.chapter_index)
        query = query.offset((page - 1) * page_size).limit(page_size)

        result = await self.session.execute(query)
        chapters = list(result.scalars().all())

        return chapters, total

    async def get_chapter(self, chapter_id: int) -> Optional[Chapter]:
        """获取单个章节"""
        result = await self.session.execute(
            select(Chapter).where(Chapter.id == chapter_id)
        )
        return result.scalar_one_or_none()

    async def update_reading_progress(
        self,
        novel_id: int,
        chapter_id: int,
        position: int = 0
    ) -> ReadingProgress:
        """更新阅读进度"""
        result = await self.session.execute(
            select(ReadingProgress).where(ReadingProgress.novel_id == novel_id)
        )
        progress = result.scalar_one_or_none()

        if progress:
            progress.last_chapter_id = chapter_id
            progress.last_position = position
        else:
            progress = ReadingProgress(
                novel_id=novel_id,
                last_chapter_id=chapter_id,
                last_position=position
            )
            self.session.add(progress)

        await self.session.commit()
        await self.session.refresh(progress)
        return progress

    async def get_reading_progress(self, novel_id: int) -> Optional[ReadingProgress]:
        """获取阅读进度"""
        result = await self.session.execute(
            select(ReadingProgress).where(ReadingProgress.novel_id == novel_id)
        )
        return result.scalar_one_or_none()
