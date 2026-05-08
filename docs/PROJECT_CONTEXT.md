# Book Scraper 项目结构上下文

## 项目概述

网络小说爬虫工具，支持多网站爬取、章节下载和在线阅读。

**技术栈：**
- 后端：Python 3.10+ / FastAPI / SQLAlchemy / Playwright / aiohttp
- 前端：Vue 3 / Element Plus / Axios / Vite
- 数据库：SQLite (aiosqlite)

---

## 目录结构

```
book-scraper/
├── backend/                    # 后端代码
│   ├── app/
│   │   ├── api/               # API路由层
│   │   ├── crawlers/          # 爬虫模块
│   │   ├── models/            # SQLAlchemy数据模型
│   │   ├── schemas/           # Pydantic验证模型
│   │   ├── services/          # 业务逻辑层
│   │   ├── config.py          # 配置管理
│   │   ├── database.py        # 数据库连接
│   │   └── main.py            # FastAPI应用入口
│   ├── rules/                 # 爬虫规则配置
│   ├── tests/                 # 测试代码
│   └── requirements.txt       # Python依赖
├── frontend/                  # 前端代码
│   ├── src/
│   │   ├── api/              # API调用封装
│   │   ├── components/       # Vue组件
│   │   ├── views/            # 页面视图
│   │   ├── router/           # 路由配置
│   │   ├── App.vue           # 根组件
│   │   └── main.js           # 入口文件
│   ├── dist/                  # 构建产物
│   └── package.json          # Node依赖
└── docs/                      # 文档
```

---

## 后端模块详解

### 1. API层 (`backend/app/api/`)

| 文件 | 职责 | 主要端点 |
|------|------|----------|
| `router.py` | 路由聚合 | - |
| `novels.py` | 小说CRUD | GET/DELETE /api/novels/{id} |
| `download.py` | 下载任务管理 | POST /api/download/start |
| `export.py` | 导出功能 | POST /api/export/txt, /api/export/epub |
| `search.py` | 搜索功能 | GET /api/search |
| `rules.py` | 规则管理 | GET/POST /api/rules |
| `settings.py` | 系统设置 | GET/PUT /api/settings |

### 2. 爬虫模块 (`backend/app/crawlers/`)

```
crawlers/
├── base.py              # 基类和数据结构
│   ├── NovelInfo        # 小说信息
│   ├── ChapterInfo      # 章节信息
│   ├── ChapterContent   # 章节内容
│   └── BaseSiteAdapter  # 适配器基类
├── anti_crawler.py      # 反爬处理器
│   └── AntiCrawlerHandler
│       ├── fetch()      # HTTP请求
│       ├── _fetch_with_js()  # Playwright渲染
│       └── cookie_jar   # Cookie管理
├── generic_adapter.py   # 通用适配器
└── adapters/            # 网站专用适配器
    ├── zongheng_adapter.py   # 纵横中文网
    ├── fanqie_adapter.py     # 番茄小说
    └── example_adapter.py    # 示例适配器
```

**适配器接口：**
```python
class BaseSiteAdapter:
    async def get_novel_info(url) -> NovelInfo
    async def get_chapter_list(url) -> List[ChapterInfo]
    async def get_chapter_content(url) -> ChapterContent
    async def close()
```

### 3. 数据模型 (`backend/app/models/`)

| 模型 | 表名 | 主要字段 |
|------|------|----------|
| Novel | novels | id, title, author, source_url, total_chapters |
| Chapter | chapters | id, novel_id, chapter_index, title, content |
| DownloadTask | download_tasks | id, novel_id, status, total_chapters, downloaded_chapters |
| SiteRule | site_rules | id, site_name, selectors, headers |
| ReadingProgress | reading_progress | id, novel_id, last_chapter_id |

### 4. 服务层 (`backend/app/services/`)

| 服务 | 职责 |
|------|------|
| NovelService | 小说CRUD、阅读进度 |
| DownloadService | 下载任务管理、后台下载 |
| ExportService | TXT/EPUB导出 |
| RuleService | 爬虫规则管理 |

### 5. 配置 (`backend/app/config.py`)

```python
class Settings:
    app_name: str = "Novel Scraper"
    database_url: str = "sqlite+aiosqlite:///./data/novels.db"
    request_delay_min: float = 1.0
    request_delay_max: float = 3.0
    max_retries: int = 3
    proxy_list: List[str] = []
    download_path: Path = Path("./data/downloads")
    auto_update_enabled: bool = False
```

---

## 前端模块详解

### 1. 页面视图 (`frontend/src/views/`)

| 组件 | 路由 | 功能 |
|------|------|------|
| Bookshelf.vue | / | 书架，显示已下载小说 |
| NovelDetail.vue | /novel/:id | 小说详情、章节列表 |
| DownloadCenter.vue | /download | 下载任务管理 |
| RuleConfig.vue | /rules | 爬虫规则配置 |
| Settings.vue | /settings | 系统设置 |

### 2. 组件 (`frontend/src/components/`)

| 组件 | 用途 |
|------|------|
| NovelCard.vue | 小说卡片（书架展示） |
| TaskItem.vue | 下载任务项 |

### 3. API封装 (`frontend/src/api/index.js`)

```javascript
// 主要API方法
getNovels(page, pageSize, tag, keyword)
getNovelDetail(id)
deleteNovel(id)
getChapters(novelId, page, pageSize)
getChapterContent(chapterId)
startDownload(url, tags)
getDownloadTasks()
pauseDownload(taskId)
resumeDownload(taskId)
cancelDownload(taskId)
exportTxt(novelId)
exportEpub(novelId)
searchNovels(keyword, type)
```

---

## 数据流

```
用户请求 → Vue组件 → API调用 → FastAPI路由 → Service层 → 数据库/爬虫
                                    ↓
                              适配器选择
                                    ↓
                    ┌───────────────┼───────────────┐
                    ↓               ↓               ↓
              ZonghengAdapter  FanqieAdapter  GenericAdapter
                    ↓               ↓               ↓
              Playwright/aiohttp → HTML解析 → 数据提取
```

---

## 关键依赖

### 后端 (requirements.txt)
```
fastapi
uvicorn
sqlalchemy[asyncio]
aiosqlite
aiohttp
beautifulsoup4
lxml
playwright
pydantic
pydantic-settings
ebooklib
python-multipart
```

### 前端 (package.json)
```
vue: ^3.x
vue-router: ^4.x
element-plus: ^2.x
axios
vite
```

---

## 网站适配器状态

| 网站 | 适配器 | 状态 | 说明 |
|------|--------|------|------|
| 纵横中文网 | ZonghengAdapter | ✅ 完整 | Playwright渲染章节列表 |
| 番茄小说 | FanqieAdapter | ⚠️ 部分 | 字体加密未解 |
| 其他 | GenericAdapter | ⚠️ 通用 | 常见选择器匹配 |

---

## 开发约定

1. **API响应格式**：使用Pydantic模型验证
2. **异步操作**：全部使用async/await
3. **数据库**：SQLAlchemy async session
4. **错误处理**：HTTPException返回错误
5. **前端状态**：Vue Composition API + ref/reactive

---

## 配置文件

| 文件 | 用途 |
|------|------|
| backend/.env | 环境变量配置 |
| backend/rules/default_rules.json | 默认爬虫规则 |
| frontend/vite.config.js | Vite构建配置 |
