# 网络小说爬虫工具设计文档

## 概述

一个基于 Python 的网络小说爬虫工具，提供 Web 界面管理下载、阅读进度、内容搜索等功能。支持特定网站适配和通用爬虫混合模式，具备高级反爬处理能力。

## 需求总结

- **界面**：Web界面（FastAPI + Vue.js）
- **爬虫模式**：混合模式（特定网站适配 + 通用爬虫后备）
- **存储**：SQLite数据库 + txt/EPUB导出
- **反爬处理**：高级防护（代理IP、JS渲染、Cookie验证等）
- **Web功能**：下载管理、进度查看、内容搜索、阅读进度、分类标签
- **规则管理**：配置文件 + Web界面
- **更新机制**：手动 + 定时自动检查

## 架构设计

### 整体架构

```
┌─────────────────────────────────────────────────────────┐
│                    Vue.js 前端                          │
│  (小说管理、下载控制、阅读进度、规则配置、搜索)          │
└─────────────────────┬───────────────────────────────────┘
                      │ HTTP/WebSocket
┌─────────────────────▼───────────────────────────────────┐
│                   FastAPI 后端                          │
├─────────────────────────────────────────────────────────┤
│  API层: 小说管理、下载控制、搜索、配置管理              │
├─────────────────────────────────────────────────────────┤
│  服务层:                                               │
│  - NovelService (小说CRUD)                             │
│  - DownloadService (下载任务管理)                       │
│  - ExportService (导出txt/EPUB)                        │
│  - UpdateService (更新检查)                            │
├─────────────────────────────────────────────────────────┤
│  爬虫引擎:                                             │
│  - SiteAdapter (网站适配器接口)                        │
│  - SpecificAdapters (特定网站适配器)                   │
│  - GenericAdapter (通用爬虫)                           │
│  - AntiCrawlerHandler (反爬处理: 代理、JS渲染等)       │
├─────────────────────────────────────────────────────────┤
│  数据层: SQLite + SQLAlchemy                           │
└─────────────────────────────────────────────────────────┘
```

### 项目结构

```
book-scraper/
├── backend/
│   ├── app/
│   │   ├── api/          # API路由
│   │   ├── models/       # 数据模型
│   │   ├── services/     # 业务逻辑
│   │   ├── crawlers/     # 爬虫引擎
│   │   │   ├── adapters/ # 网站适配器
│   │   │   ├── anti_crawler.py
│   │   │   └── base.py
│   │   ├── core/         # 配置、工具
│   │   └── main.py
│   ├── rules/            # 网站规则配置文件
│   └── data/             # SQLite数据库、下载文件
├── frontend/
│   ├── src/
│   │   ├── views/        # 页面组件
│   │   ├── components/   # 通用组件
│   │   ├── api/          # API调用
│   │   └── stores/       # 状态管理
│   └── package.json
└── docs/
```

## 技术选型

### 后端

- **FastAPI**: Web框架，异步支持好
- **SQLAlchemy + aiosqlite**: 异步ORM和SQLite驱动
- **Playwright**: 处理JS渲染页面
- **aiohttp**: 异步HTTP请求
- **BeautifulSoup4 + lxml**: HTML解析
- **EbookLib**: EPUB生成
- **APScheduler**: 定时任务（自动检查更新）

### 前端

- **Vue 3 + Composition API**: 前端框架
- **Vite**: 构建工具
- **Element Plus**: UI组件库
- **Axios**: HTTP请求

## 数据模型

### Novel（小说）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 主键 |
| title | String | 书名 |
| author | String | 作者 |
| source_url | String | 来源URL |
| source_site | String | 来源网站标识 |
| cover_url | String | 封面图片URL |
| description | Text | 简介 |
| status | String | 连载状态（连载中/已完结） |
| tags | String | 标签，逗号分隔 |
| total_chapters | Integer | 总章节数 |
| created_at | DateTime | 添加时间 |
| updated_at | DateTime | 最后更新时间 |

### Chapter（章节）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 主键 |
| novel_id | Integer | 外键关联Novel |
| chapter_index | Integer | 章节序号 |
| title | String | 章节标题 |
| content | Text | 章节内容 |
| source_url | String | 章节来源URL |
| created_at | DateTime | 创建时间 |

### SiteRule（网站规则）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 主键 |
| site_name | String | 网站名称 |
| site_url | String | 网站地址 |
| is_active | Boolean | 是否启用 |
| rule_type | String | 规则类型（specific/generic） |
| selectors | JSON | CSS选择器配置 |
| headers | JSON | 自定义请求头 |
| requires_js | Boolean | 是否需要JS渲染 |
| created_at | DateTime | 创建时间 |
| updated_at | DateTime | 更新时间 |

selectors JSON 结构：
```json
{
  "book_title": "书名选择器",
  "book_author": "作者选择器",
  "chapter_list": "章节列表选择器",
  "chapter_title": "章节标题选择器",
  "chapter_content": "内容选择器"
}
```

### DownloadTask（下载任务）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 主键 |
| novel_id | Integer | 外键 |
| status | String | 状态（pending/running/paused/completed/failed） |
| total_chapters | Integer | 总章节数 |
| downloaded_chapters | Integer | 已下载数 |
| current_chapter | String | 当前下载章节 |
| error_message | Text | 错误信息 |
| started_at | DateTime | 开始时间 |
| completed_at | DateTime | 完成时间 |

### ReadingProgress（阅读进度）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 主键 |
| novel_id | Integer | 外键 |
| last_chapter_id | Integer | 最后阅读章节 |
| last_position | Integer | 章节内位置 |
| updated_at | DateTime | 更新时间 |

## API 接口

### 小说管理

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/novels | 获取小说列表（支持分页、标签筛选） |
| GET | /api/novels/{id} | 获取小说详情 |
| DELETE | /api/novels/{id} | 删除小说 |
| GET | /api/novels/{id}/chapters | 获取章节列表 |
| GET | /api/chapters/{id} | 获取章节内容 |

### 下载控制

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/download/start | 开始下载 { url, tags? } |
| POST | /api/download/{task_id}/pause | 暂停任务 |
| POST | /api/download/{task_id}/resume | 继续任务 |
| POST | /api/download/{task_id}/cancel | 取消任务 |
| GET | /api/download/tasks | 获取任务列表 |
| GET | /api/download/{task_id} | 获取任务状态 |

### 导出功能

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/export/txt/{novel_id} | 导出txt |
| POST | /api/export/epub/{novel_id} | 导出epub |

### 搜索

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/search?keyword={keyword}&type={type} | 搜索（type: title/author/content） |

### 规则管理

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/rules | 获取规则列表 |
| GET | /api/rules/{id} | 获取规则详情 |
| POST | /api/rules | 创建规则 |
| PUT | /api/rules/{id} | 更新规则 |
| DELETE | /api/rules/{id} | 删除规则 |
| POST | /api/rules/test | 测试规则是否有效 |

### 更新检查

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/novels/{id}/check-update | 手动检查更新 |
| POST | /api/settings/auto-update | 设置自动更新配置 |
| GET | /api/settings/auto-update | 获取自动更新配置 |

## 爬虫引擎

### 下载流程

1. 用户输入小说目录页URL
2. 识别网站，匹配对应SiteRule
3. 根据规则类型选择适配器
4. 获取小说基本信息（书名、作者、简介）
5. 解析章节列表
6. 创建下载任务，逐章下载
7. 存储章节内容到数据库
8. 更新下载进度

### 反爬处理策略

- **请求频率控制**：随机延迟间隔（1-3秒）
- **User-Agent轮换**：维护UA池
- **代理IP池**：支持配置代理列表，自动轮换
- **Cookie管理**：自动保存和复用Cookie
- **JS渲染**：Playwright处理动态页面
- **失败重试**：指数退避重试（最多3次）
- **验证码处理**：检测到验证码时暂停，通知用户手动处理

### 通用适配器解析逻辑

1. 尝试常见章节列表选择器（#list、.chapter-list等）
2. 尝试常见内容选择器（#content、.content等）
3. 自动检测编码格式
4. 清理广告和无关内容
5. 如果自动解析失败，提示用户手动配置规则

## 前端页面

### 页面结构

- **书架页面**：小说卡片网格展示、标签筛选侧边栏、搜索框
- **小说详情页**：基本信息、章节列表、操作按钮、阅读进度
- **下载中心**：任务列表、实时进度更新
- **规则配置页**：规则列表、新增/编辑表单、规则测试
- **设置页面**：自动更新配置、代理设置、下载路径设置

### 核心交互

- **添加小说**：顶部输入框粘贴URL → 点击下载 → 跳转到下载中心
- **阅读章节**：点击章节 → 弹窗或新页面显示内容
- **导出**：选择格式 → 后台生成 → 浏览器下载
