import asyncio
from datetime import datetime
from typing import Optional, Dict
from urllib.parse import urlparse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Novel, Chapter, DownloadTask, SiteRule
from app.schemas import DownloadStartRequest
from app.crawlers.generic_adapter import GenericSiteAdapter
from app.crawlers.adapters import get_adapter_for_site


class DownloadService:
    # 存储运行中的任务
    _running_tasks: Dict[int, asyncio.Task] = {}

    def __init__(self, session: AsyncSession):
        self.session = session

    async def start_download(self, request: DownloadStartRequest) -> DownloadTask:
        """开始下载任务"""
        # 提取网站域名
        domain = urlparse(request.url).netloc

        # 获取网站规则
        rule = await self._get_rule_for_site(domain)

        # 创建适配器
        adapter_class = get_adapter_for_site(domain)
        if adapter_class:
            adapter = adapter_class(rule)
        else:
            adapter = GenericSiteAdapter(rule)

        # 获取小说信息
        novel_info = await adapter.get_novel_info(request.url)

        # 创建小说记录
        novel = Novel(
            title=novel_info.title,
            author=novel_info.author,
            source_url=request.url,
            source_site=domain,
            cover_url=novel_info.cover_url,
            description=novel_info.description,
            status=novel_info.status,
            tags=request.tags
        )
        self.session.add(novel)
        await self.session.flush()

        # 获取章节列表
        chapters = await adapter.get_chapter_list(request.url)
        novel.total_chapters = len(chapters)

        # 创建下载任务
        task = DownloadTask(
            novel_id=novel.id,
            status="pending",
            total_chapters=len(chapters)
        )
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)

        # 启动后台下载
        asyncio.create_task(self._download_chapters(task.id, adapter, chapters, novel.id))

        return task

    async def _download_chapters(
        self,
        task_id: int,
        adapter,
        chapters: list,
        novel_id: int
    ):
        """后台下载章节"""
        # 更新任务状态
        task = await self._get_task(task_id)
        task.status = "running"
        task.started_at = datetime.utcnow()
        await self.session.commit()

        try:
            for chapter_info in chapters:
                # 检查是否暂停
                await self.session.refresh(task)
                if task.status == "paused":
                    return

                # 下载章节
                content = await adapter.get_chapter_content(chapter_info.url)

                # 保存章节
                chapter = Chapter(
                    novel_id=novel_id,
                    chapter_index=chapter_info.index,
                    title=content.title,
                    content=content.content,
                    source_url=chapter_info.url
                )
                self.session.add(chapter)
                await self.session.flush()

                # 更新进度
                task.downloaded_chapters += 1
                task.current_chapter = content.title
                await self.session.commit()

            # 完成
            task.status = "completed"
            task.completed_at = datetime.utcnow()
            await self.session.commit()

        except Exception as e:
            task.status = "failed"
            task.error_message = str(e)
            await self.session.commit()
        finally:
            # 关闭适配器资源
            await adapter.close()

    async def pause_download(self, task_id: int) -> Optional[DownloadTask]:
        """暂停下载"""
        task = await self._get_task(task_id)
        if task and task.status == "running":
            task.status = "paused"
            await self.session.commit()
        return task

    async def resume_download(self, task_id: int) -> Optional[DownloadTask]:
        """继续下载"""
        task = await self._get_task(task_id)
        if task and task.status == "paused":
            task.status = "running"
            await self.session.commit()
            # TODO: 重新启动下载任务
        return task

    async def cancel_download(self, task_id: int) -> Optional[DownloadTask]:
        """取消下载"""
        task = await self._get_task(task_id)
        if task and task.status in ["pending", "running", "paused"]:
            task.status = "cancelled"
            await self.session.commit()
        return task

    async def get_task(self, task_id: int) -> Optional[DownloadTask]:
        """获取任务详情"""
        return await self._get_task(task_id)

    async def get_tasks(self) -> list[DownloadTask]:
        """获取所有任务"""
        result = await self.session.execute(
            select(DownloadTask).order_by(DownloadTask.created_at.desc())
        )
        return list(result.scalars().all())

    async def _get_task(self, task_id: int) -> Optional[DownloadTask]:
        result = await self.session.execute(
            select(DownloadTask).where(DownloadTask.id == task_id)
        )
        return result.scalar_one_or_none()

    async def _get_rule_for_site(self, domain: str) -> Optional[dict]:
        """获取网站规则"""
        result = await self.session.execute(
            select(SiteRule).where(
                SiteRule.site_url.contains(domain),
                SiteRule.is_active == True
            )
        )
        rule = result.scalar_one_or_none()
        if rule:
            return {
                "selectors": rule.selectors,
                "headers": rule.headers,
                "requires_js": rule.requires_js
            }
        return None
