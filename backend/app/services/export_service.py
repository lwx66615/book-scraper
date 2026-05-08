import os
from pathlib import Path
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import Novel, Chapter
from app.config import settings


class ExportService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.export_path = settings.download_path

    async def export_txt(self, novel_id: int) -> Path:
        """导出为TXT格式"""
        novel = await self._get_novel_with_chapters(novel_id)
        if not novel:
            raise ValueError("小说不存在")

        # 确保导出目录存在
        self.export_path.mkdir(parents=True, exist_ok=True)

        # 生成文件名
        filename = self._safe_filename(f"{novel.title}.txt")
        filepath = self.export_path / filename

        # 写入文件
        with open(filepath, "w", encoding="utf-8") as f:
            # 写入书名和作者
            f.write(f"{novel.title}\n")
            if novel.author:
                f.write(f"作者：{novel.author}\n")
            f.write("\n" + "=" * 50 + "\n\n")

            # 写入简介
            if novel.description:
                f.write(f"简介：\n{novel.description}\n\n")
                f.write("=" * 50 + "\n\n")

            # 写入章节
            for chapter in sorted(novel.chapters, key=lambda c: c.chapter_index):
                f.write(f"{chapter.title}\n\n")
                if chapter.content:
                    f.write(chapter.content)
                f.write("\n\n")

        return filepath

    async def export_epub(self, novel_id: int) -> Path:
        """导出为EPUB格式"""
        from ebooklib import epub

        novel = await self._get_novel_with_chapters(novel_id)
        if not novel:
            raise ValueError("小说不存在")

        # 确保导出目录存在
        self.export_path.mkdir(parents=True, exist_ok=True)

        # 创建EPUB书籍
        book = epub.EpubBook()

        # 设置元数据
        book.set_identifier(f"novel_{novel_id}")
        book.set_title(novel.title)
        if novel.author:
            book.add_author(novel.author)
        if novel.description:
            book.add_metadata("DC", "description", novel.description)

        # 创建章节
        epub_chapters = []
        toc = []
        for chapter in sorted(novel.chapters, key=lambda c: c.chapter_index):
            epub_chapter = epub.EpubHtml(
                title=chapter.title,
                file_name=f"chapter_{chapter.chapter_index}.xhtml",
                lang="zh"
            )
            epub_chapter.content = f"<h1>{chapter.title}</h1>" + \
                f"<div style='white-space: pre-wrap;'>{chapter.content or ''}</div>"
            book.add_item(epub_chapter)
            epub_chapters.append(epub_chapter)
            toc.append(epub_chapter)

        # 设置目录
        book.toc = tuple(toc)

        # 添加导航
        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())

        # 设置spine
        book.spine = ["nav"] + epub_chapters

        # 保存文件
        filename = self._safe_filename(f"{novel.title}.epub")
        filepath = self.export_path / filename
        epub.write_epub(str(filepath), book, {})

        return filepath

    async def _get_novel_with_chapters(self, novel_id: int) -> Optional[Novel]:
        result = await self.session.execute(
            select(Novel)
            .options(selectinload(Novel.chapters))
            .where(Novel.id == novel_id)
        )
        return result.scalar_one_or_none()

    def _safe_filename(self, filename: str) -> str:
        """生成安全的文件名"""
        # 移除不允许的字符
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, "_")
        return filename
