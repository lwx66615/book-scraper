from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.services.download_service import DownloadService
from app.schemas import (
    DownloadStartRequest, DownloadTaskResponse,
    DownloadTaskListResponse, MessageResponse
)

router = APIRouter()


def get_download_service(session: AsyncSession = Depends(get_session)) -> DownloadService:
    return DownloadService(session)


@router.post("/start", response_model=DownloadTaskResponse)
async def start_download(
    request: DownloadStartRequest,
    service: DownloadService = Depends(get_download_service)
):
    """开始下载"""
    try:
        task = await service.start_download(request)
        return DownloadTaskResponse.model_validate(task)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{task_id}/pause", response_model=DownloadTaskResponse)
async def pause_download(
    task_id: int,
    service: DownloadService = Depends(get_download_service)
):
    """暂停下载"""
    task = await service.pause_download(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    return DownloadTaskResponse.model_validate(task)


@router.post("/{task_id}/resume", response_model=DownloadTaskResponse)
async def resume_download(
    task_id: int,
    service: DownloadService = Depends(get_download_service)
):
    """继续下载"""
    task = await service.resume_download(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    return DownloadTaskResponse.model_validate(task)


@router.post("/{task_id}/cancel", response_model=MessageResponse)
async def cancel_download(
    task_id: int,
    service: DownloadService = Depends(get_download_service)
):
    """取消下载"""
    task = await service.cancel_download(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    return MessageResponse(message="已取消")


@router.get("/tasks", response_model=DownloadTaskListResponse)
async def get_tasks(
    service: DownloadService = Depends(get_download_service)
):
    """获取任务列表"""
    tasks = await service.get_tasks()
    return DownloadTaskListResponse(
        items=[DownloadTaskResponse.model_validate(t) for t in tasks],
        total=len(tasks)
    )


@router.get("/{task_id}", response_model=DownloadTaskResponse)
async def get_task(
    task_id: int,
    service: DownloadService = Depends(get_download_service)
):
    """获取任务状态"""
    task = await service.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    return DownloadTaskResponse.model_validate(task)
