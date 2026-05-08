# 小说爬虫工具

一个基于 Python + FastAPI + Vue.js 的网络小说爬虫工具，支持多网站爬取、章节下载和在线阅读。

## 功能特性

- 🌐 **Web界面** - 基于 Vue.js 的现代化Web界面
- 📚 **多网站支持** - 支持纵横中文网、番茄小说等多个网站
- 🔄 **智能爬取** - 自动识别网站结构，支持JS渲染页面
- 📖 **在线阅读** - 内置阅读器，支持阅读进度记录
- 📥 **批量下载** - 支持整本小说批量下载
- 📤 **导出功能** - 支持 TXT 和 EPUB 格式导出
- 🏷️ **标签管理** - 支持小说分类和标签
- 🔍 **搜索功能** - 支持按标题、作者、内容搜索

## 技术栈

### 后端
- Python 3.10+
- FastAPI - 现代异步Web框架
- SQLAlchemy + aiosqlite - 异步ORM和数据库
- Playwright - 浏览器自动化（JS渲染）
- aiohttp - 异步HTTP客户端
- BeautifulSoup4 + lxml - HTML解析
- EbookLib - EPUB生成

### 前端
- Vue 3 + Composition API
- Element Plus - UI组件库
- Axios - HTTP客户端

## 项目结构

```
book-scraper/
├── backend/                 # 后端代码
│   ├── app/
│   │   ├── api/            # API路由
│   │   ├── crawlers/       # 爬虫模块
│   │   │   ├── adapters/   # 网站适配器
│   │   │   └── anti_crawler.py  # 反爬处理
│   │   ├── models/         # 数据模型
│   │   ├── schemas/        # Pydantic模型
│   │   ├── services/       # 业务逻辑
│   │   └── main.py         # 应用入口
│   └── requirements.txt
├── frontend/               # 前端代码
│   ├── src/
│   │   ├── views/         # 页面组件
│   │   ├── components/    # 通用组件
│   │   ├── api/           # API调用
│   │   └── router/        # 路由配置
│   └── package.json
└── README.md
```

## 快速开始

### 环境要求

- Python 3.10+
- Node.js 16+
- pnpm 或 npm

### 后端安装

```bash
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 安装Playwright浏览器
playwright install chromium

# 启动服务
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 前端安装

```bash
cd frontend

# 安装依赖
pnpm install
# 或 npm install

# 开发模式
pnpm dev
# 或 npm run dev

# 构建生产版本
pnpm build
# 或 npm run build
```

### 访问应用

- 开发模式: http://localhost:5173
- 生产模式: http://localhost:8000 (前端构建后)

## 支持的网站

| 网站 | 状态 | 说明 |
|------|------|------|
| 纵横中文网 | ✅ 完整支持 | 需要JS渲染获取章节列表 |
| 番茄小说 | ⚠️ 部分支持 | 内容有字体加密 |
| 其他网站 | ⚠️ 通用适配 | 使用通用选择器尝试抓取 |

## API文档

启动后端服务后访问:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 配置说明

在 `backend/.env` 文件中配置:

```env
# 应用配置
APP_NAME=Novel Scraper
DEBUG=true

# 数据库
DATABASE_URL=sqlite+aiosqlite:///./data/novels.db

# 爬虫配置
REQUEST_DELAY_MIN=1.0
REQUEST_DELAY_MAX=3.0
MAX_RETRIES=3
PROXY_LIST=

# 自动更新
AUTO_UPDATE_ENABLED=false
AUTO_UPDATE_CRON=0 9 * * *
```

## 许可证

MIT License

## 免责声明

本项目仅供学习和研究使用，请勿用于商业用途。使用本工具爬取的内容版权归原作者所有，请支持正版。
