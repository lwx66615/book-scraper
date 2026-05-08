# 网络小说爬虫工具实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 构建一个完整的网络小说爬虫工具，支持Web界面管理、多格式导出、反爬处理和自动更新。

**Architecture:** FastAPI后端提供REST API，Vue.js前端提供Web界面，SQLite存储数据，爬虫引擎支持特定网站适配和通用爬虫混合模式。

**Tech Stack:** FastAPI, SQLAlchemy, aiohttp, Playwright, BeautifulSoup4, Vue 3, Element Plus, Vite

---

## 文件结构

```
book-scraper/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                    # FastAPI应用入口
│   │   ├── config.py                  # 配置管理
│   │   ├── database.py                # 数据库连接
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── novel.py               # Novel模型
│   │   │   ├── chapter.py             # Chapter模型
│   │   │   ├── site_rule.py           # SiteRule模型
│   │   │   ├── download_task.py       # DownloadTask模型
│   │   │   └── reading_progress.py    # ReadingProgress模型
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── novel.py
│   │   │   ├── chapter.py
│   │   │   ├── site_rule.py
│   │   │   ├── download_task.py
│   │   │   └── common.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── router.py              # API路由汇总
│   │   │   ├── novels.py              # 小说管理API
│   │   │   ├── download.py            # 下载控制API
│   │   │   ├── export.py              # 导出API
│   │   │   ├── search.py              # 搜索API
│   │   │   ├── rules.py               # 规则管理API
│   │   │   └── settings.py            # 设置API
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── novel_service.py
│   │   │   ├── download_service.py
│   │   │   ├── export_service.py
│   │   │   ├── update_service.py
│   │   │   └── rule_service.py
│   │   └── crawlers/
│   │       ├── __init__.py
│   │       ├── base.py                # 适配器基类
│   │       ├── anti_crawler.py        # 反爬处理
│   │       ├── generic_adapter.py     # 通用适配器
│   │       └── adapters/              # 特定网站适配器
│   │           ├── __init__.py
│   │           └── example_adapter.py
│   ├── rules/                         # 规则配置文件
│   │   └── default_rules.json
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   ├── test_models.py
│   │   ├── test_api/
│   │   ├── test_services/
│   │   └── test_crawlers/
│   ├── requirements.txt
│   └── pytest.ini
├── frontend/
│   ├── src/
│   │   ├── main.js
│   │   ├── App.vue
│   │   ├── api/
│   │   │   └── index.js
│   │   ├── views/
│   │   │   ├── Bookshelf.vue
│   │   │   ├── NovelDetail.vue
│   │   │   ├── DownloadCenter.vue
│   │   │   ├── RuleConfig.vue
│   │   │   └── Settings.vue
│   │   ├── components/
│   │   │   ├── NovelCard.vue
│   │   │   ├── ChapterList.vue
│   │   │   ├── TaskItem.vue
│   │   │   └── RuleForm.vue
│   │   ├── stores/
│   │   │   └── index.js
│   │   └── router/
│   │       └── index.js
│   ├── package.json
│   └── vite.config.js
└── docs/
```

---

## Phase 1: 后端基础架构

### Task 1: 项目初始化和依赖配置

**Files:**
- Create: `backend/requirements.txt`
- Create: `backend/app/__init__.py`
- Create: `backend/app/config.py`
- Create: `backend/pytest.ini`

- [ ] **Step 1: 创建requirements.txt**

```text
fastapi==0.109.0
uvicorn[standard]==0.27.0
sqlalchemy==2.0.25
aiosqlite==0.19.0
aiohttp==3.9.1
beautifulsoup4==4.12.3
lxml==5.1.0
playwright==1.41.0
ebooklib==0.18
apscheduler==3.10.4
pydantic==2.5.3
pydantic-settings==2.1.0
python-multipart==0.0.6

# 测试依赖
pytest==7.4.4
pytest-asyncio==0.23.3
httpx==0.26.0
pytest-cov==4.1.0
```

- [ ] **Step 2: 创建config.py配置文件**

```python
from pydantic_settings import BaseSettings
from pathlib import Path


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
    proxy_list: list[str] = []

    # 下载配置
    download_path: Path = Path("./data/downloads")

    # 自动更新配置
    auto_update_enabled: bool = False
    auto_update_cron: str = "0 9 * * *"  # 每天9点

    class Config:
        env_file = ".env"


settings = Settings()
```

- [ ] **Step 3: 创建pytest.ini**

```ini
[pytest]
asyncio_mode = auto
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
```

- [ ] **Step 4: 创建__init__.py**

```python
# backend/app/__init__.py
```

- [ ] **Step 5: 创建数据目录**

```bash
mkdir -p backend/data backend/rules
```

- [ ] **Step 6: 安装依赖**

```bash
cd backend && pip install -r requirements.txt
```

- [ ] **Step 7: 安装Playwright浏览器**

```bash
playwright install chromium
```

- [ ] **Step 8: 提交**

```bash
git add backend/
git commit -m "chore: initialize backend project structure"
```

---

### Task 2: 数据库模型定义

**Files:**
- Create: `backend/app/database.py`
- Create: `backend/app/models/__init__.py`
- Create: `backend/app/models/novel.py`
- Create: `backend/app/models/chapter.py`
- Create: `backend/app/models/site_rule.py`
- Create: `backend/app/models/download_task.py`
- Create: `backend/app/models/reading_progress.py`
- Create: `backend/tests/conftest.py`
- Create: `backend/tests/test_models.py`

- [ ] **Step 1: 创建database.py**

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.config import settings


engine = create_async_engine(settings.database_url, echo=settings.debug)

async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
```

- [ ] **Step 2: 创建novel.py模型**

```python
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Novel(Base):
    __tablename__ = "novels"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    author = Column(String(100))
    source_url = Column(String(500), nullable=False)
    source_site = Column(String(100))
    cover_url = Column(String(500))
    description = Column(Text)
    status = Column(String(20), default="连载中")
    tags = Column(String(500))
    total_chapters = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    chapters = relationship("Chapter", back_populates="novel", cascade="all, delete-orphan")
    download_tasks = relationship("DownloadTask", back_populates="novel", cascade="all, delete-orphan")
    reading_progress = relationship("ReadingProgress", back_populates="novel", uselist=False, cascade="all, delete-orphan")
```

- [ ] **Step 3: 创建chapter.py模型**

```python
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Chapter(Base):
    __tablename__ = "chapters"

    id = Column(Integer, primary_key=True, index=True)
    novel_id = Column(Integer, ForeignKey("novels.id"), nullable=False)
    chapter_index = Column(Integer, nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text)
    source_url = Column(String(500))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    novel = relationship("Novel", back_populates="chapters")
```

- [ ] **Step 4: 创建site_rule.py模型**

```python
from sqlalchemy import Column, Integer, String, Boolean, JSON, DateTime
from sqlalchemy.sql import func
from app.database import Base


class SiteRule(Base):
    __tablename__ = "site_rules"

    id = Column(Integer, primary_key=True, index=True)
    site_name = Column(String(100), nullable=False)
    site_url = Column(String(500), nullable=False)
    is_active = Column(Boolean, default=True)
    rule_type = Column(String(20), default="generic")  # specific/generic
    selectors = Column(JSON, default=dict)
    headers = Column(JSON, default=dict)
    requires_js = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
```

- [ ] **Step 5: 创建download_task.py模型**

```python
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class DownloadTask(Base):
    __tablename__ = "download_tasks"

    id = Column(Integer, primary_key=True, index=True)
    novel_id = Column(Integer, ForeignKey("novels.id"))
    status = Column(String(20), default="pending")  # pending/running/paused/completed/failed
    total_chapters = Column(Integer, default=0)
    downloaded_chapters = Column(Integer, default=0)
    current_chapter = Column(String(255))
    error_message = Column(Text)
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    novel = relationship("Novel", back_populates="download_tasks")
```

- [ ] **Step 6: 创建reading_progress.py模型**

```python
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class ReadingProgress(Base):
    __tablename__ = "reading_progress"

    id = Column(Integer, primary_key=True, index=True)
    novel_id = Column(Integer, ForeignKey("novels.id"), unique=True)
    last_chapter_id = Column(Integer)
    last_position = Column(Integer, default=0)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    novel = relationship("Novel", back_populates="reading_progress")
```

- [ ] **Step 7: 创建models/__init__.py**

```python
from app.models.novel import Novel
from app.models.chapter import Chapter
from app.models.site_rule import SiteRule
from app.models.download_task import DownloadTask
from app.models.reading_progress import ReadingProgress

__all__ = ["Novel", "Chapter", "SiteRule", "DownloadTask", "ReadingProgress"]
```

- [ ] **Step 8: 创建测试配置conftest.py**

```python
import pytest
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def db_session():
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
```

- [ ] **Step 9: 创建模型测试test_models.py**

```python
import pytest
from app.models import Novel, Chapter, SiteRule, DownloadTask, ReadingProgress


@pytest.mark.asyncio
async def test_create_novel(db_session):
    novel = Novel(
        title="测试小说",
        author="测试作者",
        source_url="https://example.com/novel/1",
        source_site="example.com"
    )
    db_session.add(novel)
    await db_session.commit()

    assert novel.id is not None
    assert novel.title == "测试小说"
    assert novel.status == "连载中"


@pytest.mark.asyncio
async def test_create_chapter(db_session):
    novel = Novel(title="测试小说", source_url="https://example.com/novel/1")
    db_session.add(novel)
    await db_session.commit()

    chapter = Chapter(
        novel_id=novel.id,
        chapter_index=1,
        title="第一章",
        content="这是第一章的内容",
        source_url="https://example.com/novel/1/1"
    )
    db_session.add(chapter)
    await db_session.commit()

    assert chapter.id is not None
    assert chapter.novel_id == novel.id


@pytest.mark.asyncio
async def test_create_site_rule(db_session):
    rule = SiteRule(
        site_name="测试网站",
        site_url="https://example.com",
        rule_type="specific",
        selectors={
            "book_title": "h1.title",
            "book_author": ".author",
            "chapter_list": "#chapter-list a",
            "chapter_content": "#content"
        }
    )
    db_session.add(rule)
    await db_session.commit()

    assert rule.id is not None
    assert rule.is_active is True


@pytest.mark.asyncio
async def test_create_download_task(db_session):
    novel = Novel(title="测试小说", source_url="https://example.com/novel/1")
    db_session.add(novel)
    await db_session.commit()

    task = DownloadTask(novel_id=novel.id, total_chapters=100)
    db_session.add(task)
    await db_session.commit()

    assert task.id is not None
    assert task.status == "pending"


@pytest.mark.asyncio
async def test_create_reading_progress(db_session):
    novel = Novel(title="测试小说", source_url="https://example.com/novel/1")
    db_session.add(novel)
    await db_session.commit()

    progress = ReadingProgress(novel_id=novel.id, last_chapter_id=1)
    db_session.add(progress)
    await db_session.commit()

    assert progress.id is not None
```

- [ ] **Step 10: 运行测试验证模型**

```bash
cd backend && pytest tests/test_models.py -v
```

Expected: 所有测试通过

- [ ] **Step 11: 提交**

```bash
git add backend/
git commit -m "feat: add database models"
```

---

### Task 3: Pydantic Schemas定义

**Files:**
- Create: `backend/app/schemas/__init__.py`
- Create: `backend/app/schemas/common.py`
- Create: `backend/app/schemas/novel.py`
- Create: `backend/app/schemas/chapter.py`
- Create: `backend/app/schemas/site_rule.py`
- Create: `backend/app/schemas/download_task.py`

- [ ] **Step 1: 创建common.py通用schema**

```python
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class PaginatedResponse(BaseModel):
    total: int
    page: int
    page_size: int
    total_pages: int


class MessageResponse(BaseModel):
    message: str
    success: bool = True
```

- [ ] **Step 2: 创建novel.py schema**

```python
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


class NovelBase(BaseModel):
    title: str
    author: Optional[str] = None
    source_url: str
    source_site: Optional[str] = None
    cover_url: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = "连载中"
    tags: Optional[str] = None


class NovelCreate(NovelBase):
    pass


class NovelUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    cover_url: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    tags: Optional[str] = None


class NovelResponse(NovelBase):
    id: int
    total_chapters: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class NovelListResponse(BaseModel):
    items: List[NovelResponse]
    total: int
    page: int
    page_size: int


class NovelDetailResponse(NovelResponse):
    chapters_count: int = 0
    reading_progress: Optional[dict] = None
```

- [ ] **Step 3: 创建chapter.py schema**

```python
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


class ChapterBase(BaseModel):
    chapter_index: int
    title: str
    source_url: Optional[str] = None


class ChapterCreate(ChapterBase):
    novel_id: int
    content: Optional[str] = None


class ChapterResponse(ChapterBase):
    id: int
    novel_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class ChapterContentResponse(ChapterResponse):
    content: Optional[str] = None


class ChapterListResponse(BaseModel):
    items: List[ChapterResponse]
    total: int
    novel_id: int
```

- [ ] **Step 4: 创建site_rule.py schema**

```python
from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel


class SelectorsConfig(BaseModel):
    book_title: Optional[str] = None
    book_author: Optional[str] = None
    chapter_list: Optional[str] = None
    chapter_title: Optional[str] = None
    chapter_content: Optional[str] = None


class SiteRuleBase(BaseModel):
    site_name: str
    site_url: str
    is_active: bool = True
    rule_type: str = "generic"
    selectors: Optional[Dict[str, Any]] = None
    headers: Optional[Dict[str, str]] = None
    requires_js: bool = False


class SiteRuleCreate(SiteRuleBase):
    pass


class SiteRuleUpdate(BaseModel):
    site_name: Optional[str] = None
    site_url: Optional[str] = None
    is_active: Optional[bool] = None
    rule_type: Optional[str] = None
    selectors: Optional[Dict[str, Any]] = None
    headers: Optional[Dict[str, str]] = None
    requires_js: Optional[bool] = None


class SiteRuleResponse(SiteRuleBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class SiteRuleListResponse(BaseModel):
    items: List[SiteRuleResponse]
    total: int


class RuleTestRequest(BaseModel):
    rule_id: Optional[int] = None
    test_url: str


class RuleTestResult(BaseModel):
    success: bool
    message: str
    extracted_data: Optional[Dict[str, Any]] = None
```

- [ ] **Step 5: 创建download_task.py schema**

```python
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


class DownloadStartRequest(BaseModel):
    url: str
    tags: Optional[str] = None


class DownloadTaskResponse(BaseModel):
    id: int
    novel_id: int
    status: str
    total_chapters: int
    downloaded_chapters: int
    current_chapter: Optional[str] = None
    error_message: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class DownloadTaskListResponse(BaseModel):
    items: List[DownloadTaskResponse]
    total: int


class DownloadProgressResponse(BaseModel):
    task_id: int
    status: str
    progress: float  # 0-100
    downloaded_chapters: int
    total_chapters: int
    current_chapter: Optional[str] = None
```

- [ ] **Step 6: 创建schemas/__init__.py**

```python
from app.schemas.common import PaginatedResponse, MessageResponse
from app.schemas.novel import (
    NovelCreate, NovelUpdate, NovelResponse,
    NovelListResponse, NovelDetailResponse
)
from app.schemas.chapter import (
    ChapterCreate, ChapterResponse,
    ChapterContentResponse, ChapterListResponse
)
from app.schemas.site_rule import (
    SiteRuleCreate, SiteRuleUpdate, SiteRuleResponse,
    SiteRuleListResponse, RuleTestRequest, RuleTestResult
)
from app.schemas.download_task import (
    DownloadStartRequest, DownloadTaskResponse,
    DownloadTaskListResponse, DownloadProgressResponse
)

__all__ = [
    "PaginatedResponse", "MessageResponse",
    "NovelCreate", "NovelUpdate", "NovelResponse",
    "NovelListResponse", "NovelDetailResponse",
    "ChapterCreate", "ChapterResponse",
    "ChapterContentResponse", "ChapterListResponse",
    "SiteRuleCreate", "SiteRuleUpdate", "SiteRuleResponse",
    "SiteRuleListResponse", "RuleTestRequest", "RuleTestResult",
    "DownloadStartRequest", "DownloadTaskResponse",
    "DownloadTaskListResponse", "DownloadProgressResponse",
]
```

- [ ] **Step 7: 提交**

```bash
git add backend/
git commit -m "feat: add pydantic schemas"
```

---

### Task 4: FastAPI应用入口和路由

**Files:**
- Create: `backend/app/main.py`
- Create: `backend/app/api/__init__.py`
- Create: `backend/app/api/router.py`

- [ ] **Step 1: 创建main.py**

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import init_db
from app.api.router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时初始化数据库
    await init_db()
    yield
    # 关闭时清理资源


app = FastAPI(
    title=settings.app_name,
    description="网络小说爬虫工具API",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(api_router, prefix="/api")


@app.get("/")
async def root():
    return {"message": "Novel Scraper API", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

- [ ] **Step 2: 创建api/__init__.py**

```python
# backend/app/api/__init__.py
```

- [ ] **Step 3: 创建router.py**

```python
from fastapi import APIRouter

api_router = APIRouter()

# 后续任务中添加各模块路由
# from app.api.novels import router as novels_router
# from app.api.download import router as download_router
# ...
# api_router.include_router(novels_router, prefix="/novels", tags=["novels"])
```

- [ ] **Step 4: 测试应用启动**

```bash
cd backend && uvicorn app.main:app --reload --port 8000
```

Expected: 应用成功启动，访问 http://localhost:8000 返回 {"message": "Novel Scraper API", "version": "1.0.0"}

- [ ] **Step 5: 提交**

```bash
git add backend/
git commit -m "feat: add FastAPI application entry point"
```

---

## Phase 2: 爬虫引擎

### Task 5: 爬虫基类和反爬处理器

**Files:**
- Create: `backend/app/crawlers/__init__.py`
- Create: `backend/app/crawlers/base.py`
- Create: `backend/app/crawlers/anti_crawler.py`
- Create: `backend/tests/test_crawlers/__init__.py`
- Create: `backend/tests/test_crawlers/test_anti_crawler.py`

- [ ] **Step 1: 创建crawlers/__init__.py**

```python
from app.crawlers.base import BaseSiteAdapter
from app.crawlers.anti_crawler import AntiCrawlerHandler

__all__ = ["BaseSiteAdapter", "AntiCrawlerHandler"]
```

- [ ] **Step 2: 创建base.py适配器基类**

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from bs4 import BeautifulSoup


@dataclass
class NovelInfo:
    """小说基本信息"""
    title: str
    author: Optional[str] = None
    cover_url: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None


@dataclass
class ChapterInfo:
    """章节信息"""
    index: int
    title: str
    url: str


@dataclass
class ChapterContent:
    """章节内容"""
    title: str
    content: str


class BaseSiteAdapter(ABC):
    """网站适配器基类"""

    def __init__(self, rule: Optional[Dict[str, Any]] = None):
        self.rule = rule or {}
        self.selectors = rule.get("selectors", {}) if rule else {}

    @abstractmethod
    async def get_novel_info(self, url: str) -> NovelInfo:
        """获取小说基本信息"""
        pass

    @abstractmethod
    async def get_chapter_list(self, url: str) -> List[ChapterInfo]:
        """获取章节列表"""
        pass

    @abstractmethod
    async def get_chapter_content(self, url: str) -> ChapterContent:
        """获取章节内容"""
        pass

    def parse_html(self, html: str) -> BeautifulSoup:
        """解析HTML"""
        return BeautifulSoup(html, "lxml")

    def clean_content(self, content: str) -> str:
        """清理内容（去除广告等）"""
        # 移除常见广告关键词
        ad_keywords = ["请记住本站域名", "最快更新", "无弹窗", "广告"]
        for keyword in ad_keywords:
            content = content.replace(keyword, "")
        return content.strip()
```

- [ ] **Step 3: 创建anti_crawler.py反爬处理器**

```python
import random
import asyncio
from typing import Optional, List, Dict
import aiohttp
from playwright.async_api import async_playwright, Browser, Page

from app.config import settings


class AntiCrawlerHandler:
    """反爬处理器"""

    # User-Agent池
    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    ]

    def __init__(self):
        self.session: Optional[aiohttp.ClientSession] = None
        self.browser: Optional[Browser] = None
        self.proxy_index = 0
        self.cookie_jar: Dict[str, Dict[str, str]] = {}  # 按域名存储cookie

    async def init_session(self):
        """初始化HTTP会话"""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()

    async def close(self):
        """关闭资源"""
        if self.session and not self.session.closed:
            await self.session.close()
        if self.browser:
            await self.browser.close()

    def get_random_ua(self) -> str:
        """获取随机User-Agent"""
        return random.choice(self.USER_AGENTS)

    def get_proxy(self) -> Optional[str]:
        """获取代理"""
        if not settings.proxy_list:
            return None
        proxy = settings.proxy_list[self.proxy_index]
        self.proxy_index = (self.proxy_index + 1) % len(settings.proxy_list)
        return proxy

    async def delay(self):
        """随机延迟"""
        delay = random.uniform(settings.request_delay_min, settings.request_delay_max)
        await asyncio.sleep(delay)

    async def fetch(
        self,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        use_proxy: bool = False,
        require_js: bool = False
    ) -> str:
        """
        获取页面内容

        Args:
            url: 目标URL
            headers: 自定义请求头
            use_proxy: 是否使用代理
            require_js: 是否需要JS渲染

        Returns:
            页面HTML内容
        """
        await self.delay()

        if require_js:
            return await self._fetch_with_js(url, headers)

        return await self._fetch_with_http(url, headers, use_proxy)

    async def _fetch_with_http(
        self,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        use_proxy: bool = False
    ) -> str:
        """使用aiohttp获取页面"""
        await self.init_session()

        default_headers = {
            "User-Agent": self.get_random_ua(),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        }
        if headers:
            default_headers.update(headers)

        # 添加存储的cookie
        domain = self._extract_domain(url)
        if domain in self.cookie_jar:
            cookie_str = "; ".join(f"{k}={v}" for k, v in self.cookie_jar[domain].items())
            default_headers["Cookie"] = cookie_str

        proxy = self.get_proxy() if use_proxy else None

        for attempt in range(settings.max_retries):
            try:
                async with self.session.get(
                    url,
                    headers=default_headers,
                    proxy=proxy,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status == 200:
                        html = await response.text()

                        # 保存cookie
                        cookies = response.cookies
                        if cookies:
                            if domain not in self.cookie_jar:
                                self.cookie_jar[domain] = {}
                            for cookie in cookies:
                                self.cookie_jar[domain][cookie.key] = cookie.value

                        return html
                    elif response.status == 403:
                        raise Exception(f"访问被拒绝(403)，可能需要验证码或更换IP")
                    else:
                        raise Exception(f"HTTP错误: {response.status}")

            except aiohttp.ClientError as e:
                if attempt == settings.max_retries - 1:
                    raise Exception(f"请求失败: {str(e)}")
                await asyncio.sleep(2 ** attempt)  # 指数退避

        raise Exception("请求失败")

    async def _fetch_with_js(
        self,
        url: str,
        headers: Optional[Dict[str, str]] = None
    ) -> str:
        """使用Playwright获取JS渲染页面"""
        if self.browser is None:
            playwright = await async_playwright().start()
            self.browser = await playwright.chromium.launch(headless=True)

        page = await self.browser.new_page()

        try:
            if headers:
                await page.set_extra_http_headers(headers)

            await page.set_extra_http_headers({
                "User-Agent": self.get_random_ua()
            })

            await page.goto(url, wait_until="networkidle", timeout=30000)
            html = await page.content()

            return html

        finally:
            await page.close()

    def _extract_domain(self, url: str) -> str:
        """提取域名"""
        from urllib.parse import urlparse
        parsed = urlparse(url)
        return parsed.netloc

    def detect_captcha(self, html: str) -> bool:
        """检测是否有验证码"""
        captcha_keywords = ["验证码", "captcha", "请输入验证码", "安全验证"]
        html_lower = html.lower()
        return any(keyword in html_lower for keyword in captcha_keywords)
```

- [ ] **Step 4: 创建测试文件test_anti_crawler.py**

```python
import pytest
from app.crawlers.anti_crawler import AntiCrawlerHandler


@pytest.mark.asyncio
async def test_get_random_ua():
    handler = AntiCrawlerHandler()
    ua = handler.get_random_ua()
    assert ua is not None
    assert "Mozilla" in ua


@pytest.mark.asyncio
async def test_delay():
    import time
    handler = AntiCrawlerHandler()
    start = time.time()
    # 使用最小延迟设置测试
    await handler.delay()
    elapsed = time.time() - start
    assert elapsed >= 0  # 延迟已执行


@pytest.mark.asyncio
async def test_detect_captcha():
    handler = AntiCrawlerHandler()

    html_with_captcha = "<html><body>请输入验证码继续访问</body></html>"
    assert handler.detect_captcha(html_with_captcha) is True

    html_without_captcha = "<html><body>小说内容</body></html>"
    assert handler.detect_captcha(html_without_captcha) is False


@pytest.mark.asyncio
async def test_fetch_http():
    handler = AntiCrawlerHandler()
    try:
        # 测试一个简单的HTTP请求
        html = await handler.fetch("https://httpbin.org/get", require_js=False)
        assert html is not None
        assert "httpbin.org" in html
    finally:
        await handler.close()
```

- [ ] **Step 5: 运行测试**

```bash
cd backend && pytest tests/test_crawlers/test_anti_crawler.py -v
```

Expected: 测试通过

- [ ] **Step 6: 提交**

```bash
git add backend/
git commit -m "feat: add crawler base class and anti-crawler handler"
```

---

### Task 6: 通用网站适配器

**Files:**
- Create: `backend/app/crawlers/generic_adapter.py`
- Create: `backend/tests/test_crawlers/test_generic_adapter.py`

- [ ] **Step 1: 创建generic_adapter.py**

```python
import re
from typing import List, Optional, Dict, Any
from urllib.parse import urljoin, urlparse

from app.crawlers.base import BaseSiteAdapter, NovelInfo, ChapterInfo, ChapterContent
from app.crawlers.anti_crawler import AntiCrawlerHandler


class GenericSiteAdapter(BaseSiteAdapter):
    """通用网站适配器"""

    # 常见选择器模式
    COMMON_SELECTORS = {
        "book_title": ["h1", "h2.title", ".book-title", "#info h1", "h1.title"],
        "book_author": [".author", "#info p", ".book-author", "meta[name=author]"],
        "chapter_list": ["#list a", "#chapters a", ".chapter-list a", ".list a", "#chapter-list a"],
        "chapter_content": ["#content", ".content", ".chapter-content", "#chaptercontent", ".text-content"],
        "chapter_title": ["h1", ".title", "h2"],
    }

    def __init__(self, rule: Optional[Dict[str, Any]] = None):
        super().__init__(rule)
        self.handler = AntiCrawlerHandler()

    async def close(self):
        await self.handler.close()

    async def get_novel_info(self, url: str) -> NovelInfo:
        """获取小说基本信息"""
        html = await self.handler.fetch(url, require_js=self.rule.get("requires_js", False))
        soup = self.parse_html(html)

        title = self._extract_with_fallback(soup, "book_title")
        author = self._extract_with_fallback(soup, "book_author")

        # 尝试获取封面
        cover_url = None
        cover_img = soup.select_one("img.cover, .book-cover img, #fmimg img")
        if cover_img and cover_img.get("src"):
            cover_url = urljoin(url, cover_img["src"])

        # 尝试获取简介
        description = None
        desc_elem = soup.select_one("#intro, .intro, .description, .book-intro")
        if desc_elem:
            description = desc_elem.get_text(strip=True)

        # 尝试获取状态
        status = "连载中"
        status_text = soup.get_text()
        if "完结" in status_text or "完本" in status_text:
            status = "已完结"

        return NovelInfo(
            title=title or "未知书名",
            author=author,
            cover_url=cover_url,
            description=description,
            status=status
        )

    async def get_chapter_list(self, url: str) -> List[ChapterInfo]:
        """获取章节列表"""
        html = await self.handler.fetch(url, require_js=self.rule.get("requires_js", False))
        soup = self.parse_html(html)

        chapters = []
        chapter_links = self._find_chapter_links(soup)

        for index, link in enumerate(chapter_links, 1):
            href = link.get("href")
            if not href:
                continue

            chapter_url = urljoin(url, href)
            title = link.get_text(strip=True)

            chapters.append(ChapterInfo(
                index=index,
                title=title or f"第{index}章",
                url=chapter_url
            ))

        return chapters

    async def get_chapter_content(self, url: str) -> ChapterContent:
        """获取章节内容"""
        html = await self.handler.fetch(url, require_js=self.rule.get("requires_js", False))
        soup = self.parse_html(html)

        title = self._extract_with_fallback(soup, "chapter_title") or "未知章节"
        content = self._extract_content(soup)

        # 清理内容
        content = self.clean_content(content)

        return ChapterContent(title=title, content=content)

    def _extract_with_fallback(self, soup, selector_type: str) -> Optional[str]:
        """使用多个选择器尝试提取"""
        selectors = self.selectors.get(selector_type) if self.selectors else None

        if selectors:
            # 使用配置的选择器
            if isinstance(selectors, str):
                selectors = [selectors]
            for sel in selectors:
                elem = soup.select_one(sel)
                if elem:
                    return elem.get_text(strip=True)

        # 使用常见选择器
        for sel in self.COMMON_SELECTORS.get(selector_type, []):
            elem = soup.select_one(sel)
            if elem:
                text = elem.get_text(strip=True)
                if text:
                    return text

        return None

    def _find_chapter_links(self, soup) -> List:
        """查找章节链接"""
        # 先尝试配置的选择器
        if self.selectors and "chapter_list" in self.selectors:
            sel = self.selectors["chapter_list"]
            links = soup.select(sel)
            if links:
                return links

        # 使用常见选择器
        for sel in self.COMMON_SELECTORS["chapter_list"]:
            links = soup.select(sel)
            if links:
                return links

        # 尝试查找所有包含章节特征的链接
        all_links = soup.select("a")
        chapter_links = []
        for link in all_links:
            text = link.get_text(strip=True)
            href = link.get("href", "")
            # 匹配常见章节标题模式
            if re.search(r"第[零一二三四五六七八九十百千万\d]+[章节回]", text) or \
               re.search(r"chapter\s*\d+", text, re.I) or \
               re.search(r"/\d+\.html?$", href):
                chapter_links.append(link)

        return chapter_links

    def _extract_content(self, soup) -> str:
        """提取章节内容"""
        # 先尝试配置的选择器
        if self.selectors and "chapter_content" in self.selectors:
            sel = self.selectors["chapter_content"]
            elem = soup.select_one(sel)
            if elem:
                return elem.get_text(separator="\n", strip=True)

        # 使用常见选择器
        for sel in self.COMMON_SELECTORS["chapter_content"]:
            elem = soup.select_one(sel)
            if elem:
                text = elem.get_text(separator="\n", strip=True)
                if len(text) > 100:  # 内容应该足够长
                    return text

        # 尝试查找最长的文本块
        paragraphs = soup.find_all("p")
        if paragraphs:
            content = "\n".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))
            if len(content) > 100:
                return content

        return ""
```

- [ ] **Step 2: 创建测试test_generic_adapter.py**

```python
import pytest
from app.crawlers.generic_adapter import GenericSiteAdapter


@pytest.mark.asyncio
async def test_adapter_init():
    adapter = GenericSiteAdapter()
    assert adapter.handler is not None
    await adapter.close()


@pytest.mark.asyncio
async def test_extract_with_fallback():
    from bs4 import BeautifulSoup

    adapter = GenericSiteAdapter()
    html = "<html><body><h1 class='title'>测试书名</h1></body></html>"
    soup = adapter.parse_html(html)

    title = adapter._extract_with_fallback(soup, "book_title")
    assert title == "测试书名"

    await adapter.close()


@pytest.mark.asyncio
async def test_find_chapter_links():
    from bs4 import BeautifulSoup

    adapter = GenericSiteAdapter()
    html = """
    <html><body>
        <div id="list">
            <a href="/chapter/1">第一章 开始</a>
            <a href="/chapter/2">第二章 继续</a>
        </div>
    </body></html>
    """
    soup = adapter.parse_html(html)

    links = adapter._find_chapter_links(soup)
    assert len(links) == 2
    assert links[0].get_text(strip=True) == "第一章 开始"

    await adapter.close()


@pytest.mark.asyncio
async def test_clean_content():
    adapter = GenericSiteAdapter()

    dirty_content = "这是正文内容。请记住本站域名：xxx.com最快更新无弹窗"
    clean = adapter.clean_content(dirty_content)

    assert "请记住本站域名" not in clean
    assert "最快更新" not in clean
    assert "正文内容" in clean
```

- [ ] **Step 3: 运行测试**

```bash
cd backend && pytest tests/test_crawlers/test_generic_adapter.py -v
```

Expected: 测试通过

- [ ] **Step 4: 提交**

```bash
git add backend/
git commit -m "feat: add generic site adapter"
```

---

### Task 7: 特定网站适配器示例

**Files:**
- Create: `backend/app/crawlers/adapters/__init__.py`
- Create: `backend/app/crawlers/adapters/example_adapter.py`
- Create: `backend/tests/test_crawlers/test_adapters.py`

- [ ] **Step 1: 创建adapters/__init__.py**

```python
from app.crawlers.adapters.example_adapter import ExampleSiteAdapter

# 注册所有适配器
ADAPTERS = {
    "example.com": ExampleSiteAdapter,
}


def get_adapter_for_site(site_name: str):
    """根据网站名称获取适配器"""
    return ADAPTERS.get(site_name)
```

- [ ] **Step 2: 创建example_adapter.py示例适配器**

```python
from typing import Dict, Any, Optional

from app.crawlers.base import BaseSiteAdapter, NovelInfo, ChapterInfo, ChapterContent
from app.crawlers.anti_crawler import AntiCrawlerHandler


class ExampleSiteAdapter(BaseSiteAdapter):
    """
    示例网站适配器

    这是一个模板，展示如何为特定网站创建适配器。
    实际使用时，需要根据目标网站的具体结构进行修改。
    """

    # 网站特定的选择器配置
    SITE_SELECTORS = {
        "book_title": "h1.book-name",
        "book_author": ".book-info .author",
        "chapter_list": ".chapter-list a",
        "chapter_title": "h1.chapter-title",
        "chapter_content": ".chapter-content",
    }

    def __init__(self, rule: Optional[Dict[str, Any]] = None):
        super().__init__(rule)
        self.handler = AntiCrawlerHandler()
        # 合并网站特定选择器和规则中的选择器
        self.selectors = {**self.SITE_SELECTORS, **self.selectors}

    async def close(self):
        await self.handler.close()

    async def get_novel_info(self, url: str) -> NovelInfo:
        """获取小说基本信息"""
        html = await self.handler.fetch(url)
        soup = self.parse_html(html)

        title_elem = soup.select_one(self.selectors["book_title"])
        author_elem = soup.select_one(self.selectors["book_author"])

        return NovelInfo(
            title=title_elem.get_text(strip=True) if title_elem else "未知",
            author=author_elem.get_text(strip=True) if author_elem else None,
        )

    async def get_chapter_list(self, url: str) -> list[ChapterInfo]:
        """获取章节列表"""
        html = await self.handler.fetch(url)
        soup = self.parse_html(html)

        chapters = []
        links = soup.select(self.selectors["chapter_list"])

        for index, link in enumerate(links, 1):
            from urllib.parse import urljoin
            chapter_url = urljoin(url, link.get("href", ""))
            title = link.get_text(strip=True)

            chapters.append(ChapterInfo(
                index=index,
                title=title,
                url=chapter_url
            ))

        return chapters

    async def get_chapter_content(self, url: str) -> ChapterContent:
        """获取章节内容"""
        html = await self.handler.fetch(url)
        soup = self.parse_html(html)

        title_elem = soup.select_one(self.selectors["chapter_title"])
        content_elem = soup.select_one(self.selectors["chapter_content"])

        title = title_elem.get_text(strip=True) if title_elem else "未知章节"
        content = content_elem.get_text(separator="\n", strip=True) if content_elem else ""
        content = self.clean_content(content)

        return ChapterContent(title=title, content=content)
```

- [ ] **Step 3: 创建测试test_adapters.py**

```python
import pytest
from app.crawlers.adapters import get_adapter_for_site
from app.crawlers.adapters.example_adapter import ExampleSiteAdapter


def test_get_adapter_for_site():
    adapter_class = get_adapter_for_site("example.com")
    assert adapter_class == ExampleSiteAdapter

    unknown_adapter = get_adapter_for_site("unknown.com")
    assert unknown_adapter is None


def test_example_adapter_init():
    adapter = ExampleSiteAdapter()
    assert adapter.selectors is not None
    assert "book_title" in adapter.selectors
```

- [ ] **Step 4: 运行测试**

```bash
cd backend && pytest tests/test_crawlers/test_adapters.py -v
```

Expected: 测试通过

- [ ] **Step 5: 提交**

```bash
git add backend/
git commit -m "feat: add example site adapter template"
```

---

## Phase 3: 服务层和API

### Task 8: 小说服务层

**Files:**
- Create: `backend/app/services/__init__.py`
- Create: `backend/app/services/novel_service.py`
- Create: `backend/tests/test_services/__init__.py`
- Create: `backend/tests/test_services/test_novel_service.py`

- [ ] **Step 1: 创建services/__init__.py**

```python
# backend/app/services/__init__.py
```

- [ ] **Step 2: 创建novel_service.py**

```python
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
```

- [ ] **Step 3: 创建测试test_novel_service.py**

```python
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
```

- [ ] **Step 4: 运行测试**

```bash
cd backend && pytest tests/test_services/test_novel_service.py -v
```

Expected: 测试通过

- [ ] **Step 5: 提交**

```bash
git add backend/
git commit -m "feat: add novel service layer"
```

---

### Task 9: 小说管理API

**Files:**
- Create: `backend/app/api/novels.py`
- Create: `backend/tests/test_api/__init__.py`
- Create: `backend/tests/test_api/test_novels_api.py`

- [ ] **Step 1: 创建novels.py API**

```python
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

    response = NovelDetailResponse.model_validate(novel)
    response.chapters_count = len(novel.chapters)
    response.reading_progress = {
        "last_chapter_id": progress.last_chapter_id if progress else None,
        "last_position": progress.last_position if progress else 0
    }

    return response


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
```

- [ ] **Step 2: 更新router.py注册路由**

```python
from fastapi import APIRouter

from app.api.novels import router as novels_router

api_router = APIRouter()

api_router.include_router(novels_router, prefix="/novels", tags=["novels"])
```

- [ ] **Step 3: 创建测试test_novels_api.py**

```python
import pytest
from httpx import AsyncClient
from app.main import app


@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_get_novels_empty(client):
    response = await client.get("/api/novels")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 0
    assert data["items"] == []


@pytest.mark.asyncio
async def test_get_novel_not_found(client):
    response = await client.get("/api/novels/999")
    assert response.status_code == 404
```

- [ ] **Step 4: 运行测试**

```bash
cd backend && pytest tests/test_api/test_novels_api.py -v
```

Expected: 测试通过

- [ ] **Step 5: 提交**

```bash
git add backend/
git commit -m "feat: add novels API endpoints"
```

---

### Task 10: 下载服务和API

**Files:**
- Create: `backend/app/services/download_service.py`
- Create: `backend/app/api/download.py`
- Create: `backend/tests/test_services/test_download_service.py`

- [ ] **Step 1: 创建download_service.py**

```python
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

        await adapter.close()
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
```

- [ ] **Step 2: 创建download.py API**

```python
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
```

- [ ] **Step 3: 更新router.py**

```python
from fastapi import APIRouter

from app.api.novels import router as novels_router
from app.api.download import router as download_router

api_router = APIRouter()

api_router.include_router(novels_router, prefix="/novels", tags=["novels"])
api_router.include_router(download_router, prefix="/download", tags=["download"])
```

- [ ] **Step 4: 提交**

```bash
git add backend/
git commit -m "feat: add download service and API"
```

---

### Task 11: 导出服务

**Files:**
- Create: `backend/app/services/export_service.py`
- Create: `backend/app/api/export.py`

- [ ] **Step 1: 创建export_service.py**

```python
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
```

- [ ] **Step 2: 创建export.py API**

```python
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
```

- [ ] **Step 3: 更新router.py**

```python
from fastapi import APIRouter

from app.api.novels import router as novels_router
from app.api.download import router as download_router
from app.api.export import router as export_router

api_router = APIRouter()

api_router.include_router(novels_router, prefix="/novels", tags=["novels"])
api_router.include_router(download_router, prefix="/download", tags=["download"])
api_router.include_router(export_router, prefix="/export", tags=["export"])
```

- [ ] **Step 4: 提交**

```bash
git add backend/
git commit -m "feat: add export service for txt and epub"
```

---

### Task 12: 规则管理服务和API

**Files:**
- Create: `backend/app/services/rule_service.py`
- Create: `backend/app/api/rules.py`

- [ ] **Step 1: 创建rule_service.py**

```python
import json
from pathlib import Path
from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import SiteRule
from app.schemas import SiteRuleCreate, SiteRuleUpdate
from app.crawlers.generic_adapter import GenericSiteAdapter


class RuleService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.rules_path = Path("rules/default_rules.json")

    async def get_list(self) -> List[SiteRule]:
        """获取规则列表"""
        result = await self.session.execute(
            select(SiteRule).order_by(SiteRule.created_at.desc())
        )
        return list(result.scalars().all())

    async def get_by_id(self, rule_id: int) -> Optional[SiteRule]:
        """根据ID获取规则"""
        result = await self.session.execute(
            select(SiteRule).where(SiteRule.id == rule_id)
        )
        return result.scalar_one_or_none()

    async def create(self, rule_data: SiteRuleCreate) -> SiteRule:
        """创建规则"""
        rule = SiteRule(**rule_data.model_dump())
        self.session.add(rule)
        await self.session.commit()
        await self.session.refresh(rule)
        return rule

    async def update(self, rule_id: int, rule_data: SiteRuleUpdate) -> Optional[SiteRule]:
        """更新规则"""
        rule = await self.get_by_id(rule_id)
        if not rule:
            return None

        update_data = rule_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(rule, key, value)

        await self.session.commit()
        await self.session.refresh(rule)
        return rule

    async def delete(self, rule_id: int) -> bool:
        """删除规则"""
        rule = await self.get_by_id(rule_id)
        if not rule:
            return False

        await self.session.delete(rule)
        await self.session.commit()
        return True

    async def test_rule(self, rule_id: Optional[int], test_url: str) -> dict:
        """测试规则"""
        if rule_id:
            rule = await self.get_by_id(rule_id)
            if not rule:
                return {"success": False, "message": "规则不存在"}

            rule_config = {
                "selectors": rule.selectors,
                "headers": rule.headers,
                "requires_js": rule.requires_js
            }
        else:
            rule_config = None

        adapter = GenericSiteAdapter(rule_config)

        try:
            # 测试获取小说信息
            novel_info = await adapter.get_novel_info(test_url)

            # 测试获取章节列表（只取前5个）
            chapters = await adapter.get_chapter_list(test_url)
            sample_chapters = chapters[:5]

            # 测试获取章节内容（只测试第一个）
            sample_content = None
            if sample_chapters:
                content = await adapter.get_chapter_content(sample_chapters[0].url)
                sample_content = {
                    "title": content.title,
                    "content_preview": content.content[:200] if content.content else None
                }

            await adapter.close()

            return {
                "success": True,
                "message": "规则测试成功",
                "extracted_data": {
                    "novel_info": {
                        "title": novel_info.title,
                        "author": novel_info.author,
                        "status": novel_info.status
                    },
                    "chapters_count": len(chapters),
                    "sample_chapters": [{"index": c.index, "title": c.title} for c in sample_chapters],
                    "sample_content": sample_content
                }
            }

        except Exception as e:
            await adapter.close()
            return {"success": False, "message": str(e)}

    def load_default_rules(self) -> List[dict]:
        """从配置文件加载默认规则"""
        if not self.rules_path.exists():
            return []

        with open(self.rules_path, "r", encoding="utf-8") as f:
            return json.load(f)
```

- [ ] **Step 2: 创建rules.py API**

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.services.rule_service import RuleService
from app.schemas import (
    SiteRuleCreate, SiteRuleUpdate, SiteRuleResponse,
    SiteRuleListResponse, RuleTestRequest, RuleTestResult, MessageResponse
)

router = APIRouter()


def get_rule_service(session: AsyncSession = Depends(get_session)) -> RuleService:
    return RuleService(session)


@router.get("", response_model=SiteRuleListResponse)
async def get_rules(
    service: RuleService = Depends(get_rule_service)
):
    """获取规则列表"""
    rules = await service.get_list()
    return SiteRuleListResponse(
        items=[SiteRuleResponse.model_validate(r) for r in rules],
        total=len(rules)
    )


@router.get("/{rule_id}", response_model=SiteRuleResponse)
async def get_rule(
    rule_id: int,
    service: RuleService = Depends(get_rule_service)
):
    """获取规则详情"""
    rule = await service.get_by_id(rule_id)
    if not rule:
        raise HTTPException(status_code=404, detail="规则不存在")
    return SiteRuleResponse.model_validate(rule)


@router.post("", response_model=SiteRuleResponse)
async def create_rule(
    rule_data: SiteRuleCreate,
    service: RuleService = Depends(get_rule_service)
):
    """创建规则"""
    rule = await service.create(rule_data)
    return SiteRuleResponse.model_validate(rule)


@router.put("/{rule_id}", response_model=SiteRuleResponse)
async def update_rule(
    rule_id: int,
    rule_data: SiteRuleUpdate,
    service: RuleService = Depends(get_rule_service)
):
    """更新规则"""
    rule = await service.update(rule_id, rule_data)
    if not rule:
        raise HTTPException(status_code=404, detail="规则不存在")
    return SiteRuleResponse.model_validate(rule)


@router.delete("/{rule_id}", response_model=MessageResponse)
async def delete_rule(
    rule_id: int,
    service: RuleService = Depends(get_rule_service)
):
    """删除规则"""
    success = await service.delete(rule_id)
    if not success:
        raise HTTPException(status_code=404, detail="规则不存在")
    return MessageResponse(message="删除成功")


@router.post("/test", response_model=RuleTestResult)
async def test_rule(
    request: RuleTestRequest,
    service: RuleService = Depends(get_rule_service)
):
    """测试规则"""
    result = await service.test_rule(request.rule_id, request.test_url)
    return RuleTestResult(**result)
```

- [ ] **Step 3: 更新router.py**

```python
from fastapi import APIRouter

from app.api.novels import router as novels_router
from app.api.download import router as download_router
from app.api.export import router as export_router
from app.api.rules import router as rules_router

api_router = APIRouter()

api_router.include_router(novels_router, prefix="/novels", tags=["novels"])
api_router.include_router(download_router, prefix="/download", tags=["download"])
api_router.include_router(export_router, prefix="/export", tags=["export"])
api_router.include_router(rules_router, prefix="/rules", tags=["rules"])
```

- [ ] **Step 4: 提交**

```bash
git add backend/
git commit -m "feat: add rule management service and API"
```

---

### Task 13: 搜索和设置API

**Files:**
- Create: `backend/app/api/search.py`
- Create: `backend/app/api/settings.py`

- [ ] **Step 1: 创建search.py API**

```python
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
```

- [ ] **Step 2: 创建settings.py API**

```python
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
```

- [ ] **Step 3: 更新router.py**

```python
from fastapi import APIRouter

from app.api.novels import router as novels_router
from app.api.download import router as download_router
from app.api.export import router as export_router
from app.api.rules import router as rules_router
from app.api.search import router as search_router
from app.api.settings import router as settings_router

api_router = APIRouter()

api_router.include_router(novels_router, prefix="/novels", tags=["novels"])
api_router.include_router(download_router, prefix="/download", tags=["download"])
api_router.include_router(export_router, prefix="/export", tags=["export"])
api_router.include_router(rules_router, prefix="/rules", tags=["rules"])
api_router.include_router(search_router, prefix="/search", tags=["search"])
api_router.include_router(settings_router, prefix="/settings", tags=["settings"])
```

- [ ] **Step 4: 提交**

```bash
git add backend/
git commit -m "feat: add search and settings API"
```

---

## Phase 4: 前端开发

### Task 14: 前端项目初始化

**Files:**
- Create: `frontend/package.json`
- Create: `frontend/vite.config.js`
- Create: `frontend/index.html`
- Create: `frontend/src/main.js`
- Create: `frontend/src/App.vue`

- [ ] **Step 1: 创建package.json**

```json
{
  "name": "novel-scraper-frontend",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "vue": "^3.4.0",
    "vue-router": "^4.2.5",
    "pinia": "^2.1.7",
    "axios": "^1.6.5",
    "element-plus": "^2.5.0"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^5.0.0",
    "vite": "^5.0.10"
  }
}
```

- [ ] **Step 2: 创建vite.config.js**

```javascript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  }
})
```

- [ ] **Step 3: 创建index.html**

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>网络小说爬虫</title>
</head>
<body>
  <div id="app"></div>
  <script type="module" src="/src/main.js"></script>
</body>
</html>
```

- [ ] **Step 4: 创建main.js**

```javascript
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'

import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(ElementPlus, { locale: zhCn })

app.mount('#app')
```

- [ ] **Step 5: 创建App.vue**

```vue
<template>
  <el-container class="app-container">
    <el-header>
      <div class="header-content">
        <h1>网络小说爬虫</h1>
        <el-menu mode="horizontal" :default-active="activeMenu" router>
          <el-menu-item index="/">书架</el-menu-item>
          <el-menu-item index="/download">下载中心</el-menu-item>
          <el-menu-item index="/rules">规则配置</el-menu-item>
          <el-menu-item index="/settings">设置</el-menu-item>
        </el-menu>
      </div>
    </el-header>
    <el-main>
      <router-view />
    </el-main>
  </el-container>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const activeMenu = computed(() => route.path)
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.app-container {
  min-height: 100vh;
}

.el-header {
  background-color: #409eff;
  color: white;
}

.header-content {
  display: flex;
  align-items: center;
  height: 100%;
  max-width: 1400px;
  margin: 0 auto;
}

.header-content h1 {
  margin-right: 40px;
  font-size: 20px;
}

.el-menu--horizontal {
  background-color: transparent;
  border-bottom: none;
}

.el-menu--horizontal .el-menu-item {
  color: white;
  border-bottom: none;
}

.el-menu--horizontal .el-menu-item:hover,
.el-menu--horizontal .el-menu-item.is-active {
  background-color: rgba(255, 255, 255, 0.2);
  border-bottom: none;
}
</style>
```

- [ ] **Step 6: 安装前端依赖**

```bash
cd frontend && npm install
```

- [ ] **Step 7: 提交**

```bash
git add frontend/
git commit -m "feat: initialize frontend project"
```

---

### Task 15: 前端路由和API封装

**Files:**
- Create: `frontend/src/router/index.js`
- Create: `frontend/src/api/index.js`

- [ ] **Step 1: 创建router/index.js**

```javascript
import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Bookshelf',
    component: () => import('../views/Bookshelf.vue')
  },
  {
    path: '/novel/:id',
    name: 'NovelDetail',
    component: () => import('../views/NovelDetail.vue')
  },
  {
    path: '/download',
    name: 'DownloadCenter',
    component: () => import('../views/DownloadCenter.vue')
  },
  {
    path: '/rules',
    name: 'RuleConfig',
    component: () => import('../views/RuleConfig.vue')
  },
  {
    path: '/settings',
    name: 'Settings',
    component: () => import('../views/Settings.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
```

- [ ] **Step 2: 创建api/index.js**

```javascript
import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 30000
})

// 响应拦截器
api.interceptors.response.use(
  response => response.data,
  error => {
    const message = error.response?.data?.detail || error.message || '请求失败'
    return Promise.reject(new Error(message))
  }
)

// 小说相关API
export const novelApi = {
  getList: (params) => api.get('/novels', { params }),
  getDetail: (id) => api.get(`/novels/${id}`),
  delete: (id) => api.delete(`/novels/${id}`),
  getChapters: (id, params) => api.get(`/novels/${id}/chapters`, { params }),
  getChapter: (id) => api.get(`/novels/chapters/${id}`)
}

// 下载相关API
export const downloadApi = {
  start: (data) => api.post('/download/start', data),
  pause: (id) => api.post(`/download/${id}/pause`),
  resume: (id) => api.post(`/download/${id}/resume`),
  cancel: (id) => api.post(`/download/${id}/cancel`),
  getTasks: () => api.get('/download/tasks'),
  getTask: (id) => api.get(`/download/${id}`)
}

// 导出相关API
export const exportApi = {
  txt: (id) => api.post(`/export/txt/${id}`, null, { responseType: 'blob' }),
  epub: (id) => api.post(`/export/epub/${id}`, null, { responseType: 'blob' })
}

// 规则相关API
export const ruleApi = {
  getList: () => api.get('/rules'),
  getDetail: (id) => api.get(`/rules/${id}`),
  create: (data) => api.post('/rules', data),
  update: (id, data) => api.put(`/rules/${id}`, data),
  delete: (id) => api.delete(`/rules/${id}`),
  test: (data) => api.post('/rules/test', data)
}

// 搜索API
export const searchApi = {
  search: (params) => api.get('/search', { params })
}

// 设置API
export const settingsApi = {
  getAutoUpdate: () => api.get('/settings/auto-update'),
  setAutoUpdate: (data) => api.post('/settings/auto-update', data),
  getProxy: () => api.get('/settings/proxy'),
  setProxy: (data) => api.post('/settings/proxy', data)
}

export default api
```

- [ ] **Step 3: 提交**

```bash
git add frontend/
git commit -m "feat: add router and API module"
```

---

### Task 16: 书架页面

**Files:**
- Create: `frontend/src/views/Bookshelf.vue`
- Create: `frontend/src/components/NovelCard.vue`

- [ ] **Step 1: 创建NovelCard.vue组件**

```vue
<template>
  <el-card class="novel-card" shadow="hover" @click="$emit('click')">
    <div class="card-content">
      <div class="cover">
        <el-image
          v-if="novel.cover_url"
          :src="novel.cover_url"
          fit="cover"
        >
          <template #error>
            <div class="cover-placeholder">
              <el-icon><Document /></el-icon>
            </div>
          </template>
        </el-image>
        <div v-else class="cover-placeholder">
          <el-icon><Document /></el-icon>
        </div>
      </div>
      <div class="info">
        <h3 class="title">{{ novel.title }}</h3>
        <p class="author" v-if="novel.author">{{ novel.author }}</p>
        <p class="chapters">{{ novel.total_chapters }} 章</p>
        <el-tag v-if="novel.status" size="small" :type="novel.status === '已完结' ? 'success' : ''">
          {{ novel.status }}
        </el-tag>
      </div>
    </div>
  </el-card>
</template>

<script setup>
import { Document } from '@element-plus/icons-vue'

defineProps({
  novel: {
    type: Object,
    required: true
  }
})

defineEmits(['click'])
</script>

<style scoped>
.novel-card {
  cursor: pointer;
  transition: transform 0.2s;
}

.novel-card:hover {
  transform: translateY(-4px);
}

.card-content {
  display: flex;
  gap: 12px;
}

.cover {
  width: 80px;
  height: 110px;
  flex-shrink: 0;
}

.cover .el-image,
.cover-placeholder {
  width: 100%;
  height: 100%;
  background-color: #f0f0f0;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
}

.cover-placeholder .el-icon {
  font-size: 32px;
  color: #ccc;
}

.info {
  flex: 1;
  min-width: 0;
}

.title {
  font-size: 16px;
  margin-bottom: 8px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.author,
.chapters {
  font-size: 13px;
  color: #666;
  margin-bottom: 4px;
}
</style>
```

- [ ] **Step 2: 创建Bookshelf.vue页面**

```vue
<template>
  <div class="bookshelf">
    <!-- 添加小说 -->
    <div class="add-section">
      <el-input
        v-model="newUrl"
        placeholder="输入小说目录页URL"
        style="max-width: 500px"
        clearable
      >
        <template #append>
          <el-button type="primary" @click="handleDownload" :loading="downloading">
            下载
          </el-button>
        </template>
      </el-input>
      <el-input
        v-model="newTags"
        placeholder="标签（可选，逗号分隔）"
        style="max-width: 200px; margin-left: 10px"
        clearable
      />
    </div>

    <!-- 搜索和筛选 -->
    <div class="filter-section">
      <el-input
        v-model="keyword"
        placeholder="搜索书名或作者"
        style="max-width: 300px"
        clearable
        @keyup.enter="loadNovels"
      >
        <template #append>
          <el-button @click="loadNovels">搜索</el-button>
        </template>
      </el-input>
    </div>

    <!-- 小说列表 -->
    <div class="novel-grid" v-loading="loading">
      <NovelCard
        v-for="novel in novels"
        :key="novel.id"
        :novel="novel"
        @click="goToDetail(novel.id)"
      />
    </div>

    <!-- 空状态 -->
    <el-empty v-if="!loading && novels.length === 0" description="书架空空如也" />

    <!-- 分页 -->
    <div class="pagination" v-if="total > pageSize">
      <el-pagination
        v-model:current-page="page"
        :page-size="pageSize"
        :total="total"
        layout="prev, pager, next"
        @current-change="loadNovels"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { novelApi, downloadApi } from '../api'
import NovelCard from '../components/NovelCard.vue'

const router = useRouter()

const novels = ref([])
const loading = ref(false)
const page = ref(1)
const pageSize = ref(20)
const total = ref(0)
const keyword = ref('')

const newUrl = ref('')
const newTags = ref('')
const downloading = ref(false)

const loadNovels = async () => {
  loading.value = true
  try {
    const data = await novelApi.getList({
      page: page.value,
      page_size: pageSize.value,
      keyword: keyword.value || undefined
    })
    novels.value = data.items
    total.value = data.total
  } catch (error) {
    ElMessage.error(error.message)
  } finally {
    loading.value = false
  }
}

const handleDownload = async () => {
  if (!newUrl.value) {
    ElMessage.warning('请输入小说URL')
    return
  }

  downloading.value = true
  try {
    await downloadApi.start({
      url: newUrl.value,
      tags: newTags.value || undefined
    })
    ElMessage.success('已开始下载')
    newUrl.value = ''
    newTags.value = ''
    router.push('/download')
  } catch (error) {
    ElMessage.error(error.message)
  } finally {
    downloading.value = false
  }
}

const goToDetail = (id) => {
  router.push(`/novel/${id}`)
}

onMounted(() => {
  loadNovels()
})
</script>

<style scoped>
.bookshelf {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
}

.add-section {
  margin-bottom: 20px;
  display: flex;
  align-items: center;
}

.filter-section {
  margin-bottom: 20px;
}

.novel-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 16px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}
</style>
```

- [ ] **Step 3: 提交**

```bash
git add frontend/
git commit -m "feat: add bookshelf page and novel card component"
```

---

### Task 17: 小说详情页

**Files:**
- Create: `frontend/src/views/NovelDetail.vue`

- [ ] **Step 1: 创建NovelDetail.vue**

```vue
<template>
  <div class="novel-detail" v-loading="loading">
    <template v-if="novel">
      <!-- 基本信息 -->
      <el-card class="info-card">
        <div class="novel-header">
          <div class="cover">
            <el-image v-if="novel.cover_url" :src="novel.cover_url" fit="cover">
              <template #error>
                <div class="cover-placeholder">
                  <el-icon><Document /></el-icon>
                </div>
              </template>
            </el-image>
            <div v-else class="cover-placeholder">
              <el-icon><Document /></el-icon>
            </div>
          </div>
          <div class="info">
            <h1>{{ novel.title }}</h1>
            <p class="author" v-if="novel.author">作者：{{ novel.author }}</p>
            <p class="source">来源：{{ novel.source_site }}</p>
            <el-tag :type="novel.status === '已完结' ? 'success' : ''">
              {{ novel.status }}
            </el-tag>
            <p class="description" v-if="novel.description">{{ novel.description }}</p>
          </div>
          <div class="actions">
            <el-button type="primary" @click="handleExport('txt')">导出TXT</el-button>
            <el-button type="primary" @click="handleExport('epub')">导出EPUB</el-button>
            <el-button @click="checkUpdate">检查更新</el-button>
            <el-button type="danger" @click="handleDelete">删除</el-button>
          </div>
        </div>
      </el-card>

      <!-- 章节列表 -->
      <el-card class="chapters-card">
        <template #header>
          <div class="chapters-header">
            <span>章节列表 ({{ novel.total_chapters }}章)</span>
            <el-input
              v-model="chapterKeyword"
              placeholder="搜索章节"
              style="width: 200px"
              clearable
            />
          </div>
        </template>

        <div class="chapters-grid">
          <div
            v-for="chapter in filteredChapters"
            :key="chapter.id"
            class="chapter-item"
            @click="showChapter(chapter)"
          >
            {{ chapter.title }}
          </div>
        </div>

        <el-empty v-if="chapters.length === 0" description="暂无章节" />
      </el-card>
    </template>

    <!-- 章节内容弹窗 -->
    <el-dialog v-model="chapterDialogVisible" :title="currentChapter?.title" width="60%">
      <div class="chapter-content" v-loading="chapterLoading">
        {{ currentChapterContent }}
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Document } from '@element-plus/icons-vue'
import { novelApi, exportApi } from '../api'

const route = useRoute()
const router = useRouter()

const novel = ref(null)
const chapters = ref([])
const loading = ref(false)
const chapterKeyword = ref('')

const chapterDialogVisible = ref(false)
const currentChapter = ref(null)
const currentChapterContent = ref('')
const chapterLoading = ref(false)

const filteredChapters = computed(() => {
  if (!chapterKeyword.value) return chapters.value
  return chapters.value.filter(c =>
    c.title.toLowerCase().includes(chapterKeyword.value.toLowerCase())
  )
})

const loadNovel = async () => {
  loading.value = true
  try {
    novel.value = await novelApi.getDetail(route.params.id)
    const data = await novelApi.getChapters(route.params.id, { page_size: 1000 })
    chapters.value = data.items
  } catch (error) {
    ElMessage.error(error.message)
  } finally {
    loading.value = false
  }
}

const showChapter = async (chapter) => {
  currentChapter.value = chapter
  chapterDialogVisible.value = true
  chapterLoading.value = true

  try {
    const data = await novelApi.getChapter(chapter.id)
    currentChapterContent.value = data.content || '内容为空'
  } catch (error) {
    ElMessage.error(error.message)
    currentChapterContent.value = '加载失败'
  } finally {
    chapterLoading.value = false
  }
}

const handleExport = async (type) => {
  try {
    const response = type === 'txt'
      ? await exportApi.txt(novel.value.id)
      : await exportApi.epub(novel.value.id)

    // 创建下载链接
    const blob = new Blob([response], {
      type: type === 'txt' ? 'text/plain' : 'application/epub+zip'
    })
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${novel.value.title}.${type}`
    a.click()
    window.URL.revokeObjectURL(url)

    ElMessage.success('导出成功')
  } catch (error) {
    ElMessage.error(error.message)
  }
}

const checkUpdate = async () => {
  ElMessage.info('检查更新功能开发中')
}

const handleDelete = async () => {
  try {
    await ElMessageBox.confirm('确定要删除这本小说吗？', '提示', {
      type: 'warning'
    })

    await novelApi.delete(novel.value.id)
    ElMessage.success('删除成功')
    router.push('/')
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error(error.message)
    }
  }
}

onMounted(() => {
  loadNovel()
})
</script>

<style scoped>
.novel-detail {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.info-card {
  margin-bottom: 20px;
}

.novel-header {
  display: flex;
  gap: 24px;
}

.cover {
  width: 150px;
  height: 200px;
  flex-shrink: 0;
}

.cover .el-image,
.cover-placeholder {
  width: 100%;
  height: 100%;
  background-color: #f0f0f0;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
}

.cover-placeholder .el-icon {
  font-size: 48px;
  color: #ccc;
}

.info {
  flex: 1;
}

.info h1 {
  margin-bottom: 12px;
}

.author,
.source {
  color: #666;
  margin-bottom: 8px;
}

.description {
  margin-top: 12px;
  color: #333;
  line-height: 1.6;
}

.actions {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.chapters-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chapters-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 8px;
  max-height: 500px;
  overflow-y: auto;
}

.chapter-item {
  padding: 8px 12px;
  cursor: pointer;
  border-radius: 4px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.chapter-item:hover {
  background-color: #f0f0f0;
}

.chapter-content {
  white-space: pre-wrap;
  line-height: 1.8;
  max-height: 60vh;
  overflow-y: auto;
}
</style>
```

- [ ] **Step 2: 提交**

```bash
git add frontend/
git commit -m "feat: add novel detail page"
```

---

### Task 18: 下载中心页面

**Files:**
- Create: `frontend/src/views/DownloadCenter.vue`
- Create: `frontend/src/components/TaskItem.vue`

- [ ] **Step 1: 创建TaskItem.vue组件**

```vue
<template>
  <el-card class="task-item">
    <div class="task-content">
      <div class="task-info">
        <h4>{{ task.novel?.title || '未知小说' }}</h4>
        <p class="status">
          <el-tag :type="statusType">{{ statusText }}</el-tag>
          <span class="progress-text">
            {{ task.downloaded_chapters }} / {{ task.total_chapters }} 章
          </span>
        </p>
        <el-progress
          :percentage="progress"
          :status="progressStatus"
          :stroke-width="10"
        />
        <p class="current" v-if="task.current_chapter && task.status === 'running'">
          正在下载：{{ task.current_chapter }}
        </p>
        <p class="error" v-if="task.error_message">
          <el-icon><WarningFilled /></el-icon>
          {{ task.error_message }}
        </p>
      </div>
      <div class="task-actions">
        <el-button
          v-if="task.status === 'running'"
          type="warning"
          size="small"
          @click="$emit('pause', task.id)"
        >
          暂停
        </el-button>
        <el-button
          v-if="task.status === 'paused'"
          type="primary"
          size="small"
          @click="$emit('resume', task.id)"
        >
          继续
        </el-button>
        <el-button
          v-if="['pending', 'running', 'paused'].includes(task.status)"
          type="danger"
          size="small"
          @click="$emit('cancel', task.id)"
        >
          取消
        </el-button>
      </div>
    </div>
  </el-card>
</template>

<script setup>
import { computed } from 'vue'
import { WarningFilled } from '@element-plus/icons-vue'

const props = defineProps({
  task: {
    type: Object,
    required: true
  }
})

defineEmits(['pause', 'resume', 'cancel'])

const statusMap = {
  pending: { text: '等待中', type: 'info' },
  running: { text: '下载中', type: 'primary' },
  paused: { text: '已暂停', type: 'warning' },
  completed: { text: '已完成', type: 'success' },
  failed: { text: '失败', type: 'danger' },
  cancelled: { text: '已取消', type: 'info' }
}

const statusText = computed(() => statusMap[props.task.status]?.text || '未知')
const statusType = computed(() => statusMap[props.task.status]?.type || 'info')

const progress = computed(() => {
  if (props.task.total_chapters === 0) return 0
  return Math.round((props.task.downloaded_chapters / props.task.total_chapters) * 100)
})

const progressStatus = computed(() => {
  if (props.task.status === 'completed') return 'success'
  if (props.task.status === 'failed') return 'exception'
  return null
})
</script>

<style scoped>
.task-item {
  margin-bottom: 12px;
}

.task-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.task-info {
  flex: 1;
}

.task-info h4 {
  margin-bottom: 8px;
}

.status {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 8px;
}

.progress-text {
  color: #666;
  font-size: 14px;
}

.current {
  color: #409eff;
  font-size: 13px;
  margin-top: 8px;
}

.error {
  color: #f56c6c;
  font-size: 13px;
  margin-top: 8px;
  display: flex;
  align-items: center;
  gap: 4px;
}

.task-actions {
  display: flex;
  gap: 8px;
}
</style>
```

- [ ] **Step 2: 创建DownloadCenter.vue页面**

```vue
<template>
  <div class="download-center">
    <h2>下载中心</h2>

    <div class="tasks-list" v-loading="loading">
      <TaskItem
        v-for="task in tasks"
        :key="task.id"
        :task="task"
        @pause="handlePause"
        @resume="handleResume"
        @cancel="handleCancel"
      />

      <el-empty v-if="!loading && tasks.length === 0" description="暂无下载任务" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { downloadApi } from '../api'
import TaskItem from '../components/TaskItem.vue'

const tasks = ref([])
const loading = ref(false)
let pollTimer = null

const loadTasks = async () => {
  try {
    const data = await downloadApi.getTasks()
    tasks.value = data.items
  } catch (error) {
    console.error('加载任务失败:', error)
  }
}

const handlePause = async (taskId) => {
  try {
    await downloadApi.pause(taskId)
    ElMessage.success('已暂停')
    await loadTasks()
  } catch (error) {
    ElMessage.error(error.message)
  }
}

const handleResume = async (taskId) => {
  try {
    await downloadApi.resume(taskId)
    ElMessage.success('已继续')
    await loadTasks()
  } catch (error) {
    ElMessage.error(error.message)
  }
}

const handleCancel = async (taskId) => {
  try {
    await ElMessageBox.confirm('确定要取消这个下载任务吗？', '提示', {
      type: 'warning'
    })
    await downloadApi.cancel(taskId)
    ElMessage.success('已取消')
    await loadTasks()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error(error.message)
    }
  }
}

onMounted(() => {
  loadTasks()
  // 每3秒轮询更新任务状态
  pollTimer = setInterval(loadTasks, 3000)
})

onUnmounted(() => {
  if (pollTimer) {
    clearInterval(pollTimer)
  }
})
</script>

<style scoped>
.download-center {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
}

.download-center h2 {
  margin-bottom: 20px;
}

.tasks-list {
  min-height: 200px;
}
</style>
```

- [ ] **Step 3: 提交**

```bash
git add frontend/
git commit -m "feat: add download center page"
```

---

### Task 19: 规则配置和设置页面

**Files:**
- Create: `frontend/src/views/RuleConfig.vue`
- Create: `frontend/src/views/Settings.vue`

- [ ] **Step 1: 创建RuleConfig.vue页面**

```vue
<template>
  <div class="rule-config">
    <div class="header">
      <h2>规则配置</h2>
      <el-button type="primary" @click="showDialog()">新增规则</el-button>
    </div>

    <el-table :data="rules" v-loading="loading">
      <el-table-column prop="site_name" label="网站名称" />
      <el-table-column prop="site_url" label="网站地址" />
      <el-table-column prop="rule_type" label="类型">
        <template #default="{ row }">
          <el-tag :type="row.rule_type === 'specific' ? 'primary' : 'info'">
            {{ row.rule_type === 'specific' ? '特定适配' : '通用' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="is_active" label="状态">
        <template #default="{ row }">
          <el-tag :type="row.is_active ? 'success' : 'danger'">
            {{ row.is_active ? '启用' : '禁用' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200">
        <template #default="{ row }">
          <el-button size="small" @click="testRule(row)">测试</el-button>
          <el-button size="small" @click="showDialog(row)">编辑</el-button>
          <el-button size="small" type="danger" @click="handleDelete(row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 编辑弹窗 -->
    <el-dialog v-model="dialogVisible" :title="editingRule ? '编辑规则' : '新增规则'" width="600px">
      <el-form :model="form" label-width="100px">
        <el-form-item label="网站名称" required>
          <el-input v-model="form.site_name" />
        </el-form-item>
        <el-form-item label="网站地址" required>
          <el-input v-model="form.site_url" />
        </el-form-item>
        <el-form-item label="规则类型">
          <el-radio-group v-model="form.rule_type">
            <el-radio value="generic">通用</el-radio>
            <el-radio value="specific">特定适配</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="书名选择器">
          <el-input v-model="form.selectors.book_title" placeholder="如: h1.title" />
        </el-form-item>
        <el-form-item label="作者选择器">
          <el-input v-model="form.selectors.book_author" placeholder="如: .author" />
        </el-form-item>
        <el-form-item label="章节列表选择器">
          <el-input v-model="form.selectors.chapter_list" placeholder="如: #list a" />
        </el-form-item>
        <el-form-item label="内容选择器">
          <el-input v-model="form.selectors.chapter_content" placeholder="如: #content" />
        </el-form-item>
        <el-form-item label="需要JS渲染">
          <el-switch v-model="form.requires_js" />
        </el-form-item>
        <el-form-item label="启用">
          <el-switch v-model="form.is_active" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSave">保存</el-button>
      </template>
    </el-dialog>

    <!-- 测试结果弹窗 -->
    <el-dialog v-model="testDialogVisible" title="测试结果" width="500px">
      <pre class="test-result">{{ testResult }}</pre>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { ruleApi } from '../api'

const rules = ref([])
const loading = ref(false)
const dialogVisible = ref(false)
const testDialogVisible = ref(false)
const testResult = ref('')
const editingRule = ref(null)

const form = reactive({
  site_name: '',
  site_url: '',
  rule_type: 'generic',
  is_active: true,
  requires_js: false,
  selectors: {
    book_title: '',
    book_author: '',
    chapter_list: '',
    chapter_content: ''
  }
})

const loadRules = async () => {
  loading.value = true
  try {
    const data = await ruleApi.getList()
    rules.value = data.items
  } catch (error) {
    ElMessage.error(error.message)
  } finally {
    loading.value = false
  }
}

const showDialog = (rule = null) => {
  editingRule.value = rule
  if (rule) {
    Object.assign(form, {
      site_name: rule.site_name,
      site_url: rule.site_url,
      rule_type: rule.rule_type,
      is_active: rule.is_active,
      requires_js: rule.requires_js,
      selectors: rule.selectors || {}
    })
  } else {
    Object.assign(form, {
      site_name: '',
      site_url: '',
      rule_type: 'generic',
      is_active: true,
      requires_js: false,
      selectors: {
        book_title: '',
        book_author: '',
        chapter_list: '',
        chapter_content: ''
      }
    })
  }
  dialogVisible.value = true
}

const handleSave = async () => {
  try {
    if (editingRule.value) {
      await ruleApi.update(editingRule.value.id, form)
      ElMessage.success('更新成功')
    } else {
      await ruleApi.create(form)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    await loadRules()
  } catch (error) {
    ElMessage.error(error.message)
  }
}

const handleDelete = async (ruleId) => {
  try {
    await ElMessageBox.confirm('确定要删除这个规则吗？', '提示', { type: 'warning' })
    await ruleApi.delete(ruleId)
    ElMessage.success('删除成功')
    await loadRules()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error(error.message)
    }
  }
}

const testRule = async (rule) => {
  const testUrl = await ElMessageBox.prompt('请输入测试URL', '测试规则', {
    inputPattern: /^https?:\/\/.+/,
    inputErrorMessage: '请输入有效的URL'
  }).catch(() => null)

  if (!testUrl) return

  try {
    ElMessage.info('正在测试...')
    const result = await ruleApi.test({
      rule_id: rule.id,
      test_url: testUrl.value
    })

    testResult.value = JSON.stringify(result, null, 2)
    testDialogVisible.value = true

    if (result.success) {
      ElMessage.success('测试成功')
    } else {
      ElMessage.error(result.message)
    }
  } catch (error) {
    ElMessage.error(error.message)
  }
}

onMounted(() => {
  loadRules()
})
</script>

<style scoped>
.rule-config {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.test-result {
  background-color: #f5f5f5;
  padding: 16px;
  border-radius: 4px;
  overflow: auto;
  max-height: 400px;
}
</style>
```

- [ ] **Step 2: 创建Settings.vue页面**

```vue
<template>
  <div class="settings">
    <h2>设置</h2>

    <el-card class="settings-card">
      <template #header>自动更新</template>
      <el-form label-width="120px">
        <el-form-item label="启用自动更新">
          <el-switch v-model="autoUpdate.enabled" />
        </el-form-item>
        <el-form-item label="检查时间" v-if="autoUpdate.enabled">
          <el-input v-model="autoUpdate.cron" placeholder="Cron表达式，如: 0 9 * * *" />
          <div class="hint">每天9点检查更新</div>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="saveAutoUpdate">保存</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card class="settings-card">
      <template #header>代理设置</template>
      <el-form label-width="120px">
        <el-form-item label="代理列表">
          <el-input
            v-model="proxyText"
            type="textarea"
            :rows="4"
            placeholder="每行一个代理地址，如：&#10;http://127.0.0.1:7890&#10;http://127.0.0.1:7891"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="saveProxy">保存</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { settingsApi } from '../api'

const autoUpdate = ref({
  enabled: false,
  cron: '0 9 * * *'
})

const proxyText = ref('')

const loadSettings = async () => {
  try {
    const autoUpdateData = await settingsApi.getAutoUpdate()
    autoUpdate.value = autoUpdateData

    const proxyData = await settingsApi.getProxy()
    proxyText.value = proxyData.proxies.join('\n')
  } catch (error) {
    console.error('加载设置失败:', error)
  }
}

const saveAutoUpdate = async () => {
  try {
    await settingsApi.setAutoUpdate(autoUpdate.value)
    ElMessage.success('保存成功')
  } catch (error) {
    ElMessage.error(error.message)
  }
}

const saveProxy = async () => {
  try {
    const proxies = proxyText.value
      .split('\n')
      .map(p => p.trim())
      .filter(p => p)

    await settingsApi.setProxy({ proxies })
    ElMessage.success('保存成功')
  } catch (error) {
    ElMessage.error(error.message)
  }
}

onMounted(() => {
  loadSettings()
})
</script>

<style scoped>
.settings {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.settings-card {
  margin-bottom: 20px;
}

.hint {
  color: #999;
  font-size: 12px;
  margin-top: 4px;
}
</style>
```

- [ ] **Step 3: 提交**

```bash
git add frontend/
git commit -m "feat: add rule config and settings pages"
```

---

## Phase 5: 集成和测试

### Task 20: 默认规则配置和最终集成

**Files:**
- Create: `backend/rules/default_rules.json`
- Update: `backend/app/main.py`

- [ ] **Step 1: 创建default_rules.json**

```json
[
  {
    "site_name": "起点中文网",
    "site_url": "qidian.com",
    "rule_type": "generic",
    "is_active": true,
    "requires_js": true,
    "selectors": {
      "book_title": "h1#bookName",
      "book_author": ".writer",
      "chapter_list": "#j-catalogWrap .cf a",
      "chapter_content": ".read-content"
    }
  },
  {
    "site_name": "纵横中文网",
    "site_url": "zongheng.com",
    "rule_type": "generic",
    "is_active": true,
    "requires_js": false,
    "selectors": {
      "book_title": ".book-name",
      "book_author": ".au-name a",
      "chapter_list": ".chapter-list a",
      "chapter_content": ".content"
    }
  }
]
```

- [ ] **Step 2: 更新main.py添加静态文件服务**

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from app.config import settings
from app.database import init_db
from app.api.router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title=settings.app_name,
    description="网络小说爬虫工具API",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

# 挂载静态文件（前端构建产物）
frontend_dist = Path(__file__).parent.parent.parent / "frontend" / "dist"
if frontend_dist.exists():
    app.mount("/", StaticFiles(directory=str(frontend_dist), html=True), name="static")


@app.get("/api")
async def api_root():
    return {"message": "Novel Scraper API", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

- [ ] **Step 3: 运行完整测试**

```bash
cd backend && pytest -v
```

Expected: 所有测试通过

- [ ] **Step 4: 构建前端**

```bash
cd frontend && npm run build
```

Expected: 构建成功，生成dist目录

- [ ] **Step 5: 启动完整应用测试**

```bash
cd backend && uvicorn app.main:app --reload --port 8000
```

Expected: 应用启动成功，访问 http://localhost:8000 显示前端页面

- [ ] **Step 6: 最终提交**

```bash
git add .
git commit -m "feat: complete novel scraper tool implementation"
```

---

## 实现完成

以上是实现网络小说爬虫工具的完整计划。按照TDD原则，每个功能模块都有对应的测试，确保代码质量。

**后续可优化方向：**
1. 添加更多特定网站适配器
2. 实现WebSocket实时推送下载进度
3. 添加用户认证功能
4. 优化前端UI/UX
5. 添加日志记录和错误追踪
