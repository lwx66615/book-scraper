from pydantic_settings import BaseSettings
from pydantic import field_validator
from pathlib import Path
from typing import List


class Settings(BaseSettings):
    # 应用配置
    app_name: str = "Novel Scraper"
    debug: bool = True

    # 数据库配置
    database_url: str = "sqlite+aiosqlite:///./data/novels.db"

    # 爬虫配置
    request_delay_min: float = 1.0
    request_delay_max: float = 3.0
    max_retries: int = 3
    proxy_list: List[str] = []

    # 下载配置
    download_path: Path = Path("./data/downloads")

    # 自动更新配置
    auto_update_enabled: bool = False
    auto_update_cron: str = "0 9 * * *"  # 每天9点

    @field_validator('proxy_list', mode='before')
    @classmethod
    def parse_proxy_list(cls, v):
        if isinstance(v, str):
            # 如果是字符串，按逗号分割
            return [p.strip() for p in v.split(',') if p.strip()]
        return v or []

    class Config:
        env_file = ".env"


settings = Settings()
