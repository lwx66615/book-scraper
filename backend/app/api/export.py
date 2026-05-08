from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.services.export_service import ExportService

router = APIRouter()


@router.post("/txt/{novel_id}")
async def export_txt(
    novel_id: int,
    session: AsyncSession = Depends(get_session)
):
    """导出TXT格式"""
    service = ExportService(session)
    try:
        filepath = await service.export_txt(novel_id)
        return FileResponse(
            path=filepath,
            filename=filepath.name,
            media_type="text/plain"
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/epub/{novel_id}")
async def export_epub(
    novel_id: int,
    session: AsyncSession = Depends(get_session)
):
    """导出EPUB格式"""
    service = ExportService(session)
    try:
        filepath = await service.export_epub(novel_id)
        return FileResponse(
            path=filepath,
            filename=filepath.name,
            media_type="application/epub+zip"
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
