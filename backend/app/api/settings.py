from fastapi import APIRouter
from pydantic import BaseModel

from app.config import settings

router = APIRouter()


class AutoUpdateSettings(BaseModel):
    enabled: bool = False
    cron: str = "0 9 * * *"


class ProxySettings(BaseModel):
    proxies: list[str] = []


# 内存中存储设置（实际项目中应该持久化）
_auto_update_settings = AutoUpdateSettings()
_proxy_settings = ProxySettings()


@router.get("/auto-update", response_model=AutoUpdateSettings)
async def get_auto_update_settings():
    """获取自动更新设置"""
    return _auto_update_settings


@router.post("/auto-update", response_model=AutoUpdateSettings)
async def set_auto_update_settings(data: AutoUpdateSettings):
    """设置自动更新"""
    _auto_update_settings.enabled = data.enabled
    _auto_update_settings.cron = data.cron
    return _auto_update_settings


@router.get("/proxy", response_model=ProxySettings)
async def get_proxy_settings():
    """获取代理设置"""
    return _proxy_settings


@router.post("/proxy", response_model=ProxySettings)
async def set_proxy_settings(data: ProxySettings):
    """设置代理"""
    _proxy_settings.proxies = data.proxies
    # 更新全局设置
    settings.proxy_list = data.proxies
    return _proxy_settings
