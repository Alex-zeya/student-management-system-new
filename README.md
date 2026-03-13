# 学生课程管理系统

基于 Django REST Framework + React 的前后端分离学生课程管理系统。

## 项目结构

```
student-system/
├── backend/                 # Django 后端
│   ├── student_system/     # Django 项目配置
│   ├── users/              # 用户管理应用
│   ├── courses/            # 课程管理应用
│   ├── tasks/             # 任务管理应用
│   ├── resources/         # 资源管理应用
│   ├── announcements/     # 公告管理应用
│   └── venv/              # Python 虚拟环境
│
└── frontend/              # React 前端
    ├── src/
    │   ├── api/           # API 接口
    │   ├── components/    # 组件
    │   ├── context/       # React Context
    │   ├── pages/         # 页面组件
    │   └── types/         # TypeScript 类型定义
    └── node_modules/      # 前端依赖
```

## 功能特性

### 用户角色
- **学生**: 查看课程、完成任务、追踪进度、查看资源与公告
- **教师**: 创建课程、发布任务与资源、发布公告、评分
- **管理员**: 用户管理、课程管理、系统维护

### 核心功能
- 用户认证与权限控制 (基于 Token)
- 课程管理 (创建、更新、选课、退课)
- 任务管理 (发布、提交、评分)
- 学习资源管理
- 课程公告
- 学习进度追踪

## 技术栈

### 后端
- Django 5.2
- Django REST Framework
- Django CORS Headers
- SQLite (开发环境)

### 前端
- React 18
- TypeScript
- Vite
- React Router
- Axios
- Tailwind CSS

## 环境要求

- Python 3.8+
- Node.js 14+
- npm 或 yarn

## 安装与运行

### 1. 克隆项目

### 2. 后端设置

```bash
# 进入后端目录
cd backend

# 创建虚拟环境 (可选)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt

# 数据库迁移
python manage.py migrate

# 创建超级用户 (可选)
python manage.py createsuperuser

# 启动开发服务器
python manage.py runserver
```

后端服务将在 http://localhost:8000 运行

### 3. 前端设置

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端服务将在 http://localhost:5173 运行

## API 接口

| 方法 | 路径 | 描述 |
|------|------|------|
| POST | /api/auth/login/ | 用户登录 |
| POST | /api/auth/register/ | 用户注册 |
| POST | /api/auth/logout/ | 用户登出 |
| GET | /api/auth/me/ | 获取当前用户 |
| GET | /api/courses/ | 获取课程列表 |
| POST | /api/courses/{id}/enroll/ | 选课 |
| POST | /api/courses/{id}/drop/ | 退课 |
| GET | /api/courses/my_courses/ | 获取已选课程 |
| GET | /api/tasks/my_tasks/ | 获取学生任务 |
| POST | /api/submissions/ | 提交任务 |
| POST | /api/submissions/{id}/grade/ | 评分 |

## 快速开始

1. 启动后端服务器: `cd backend && python manage.py runserver`
2. 启动前端服务器: `cd frontend && npm run dev`
3. 访问 http://localhost:5173
4. 注册新用户或使用管理员账号登录

## 注意事项

- 前端默认代理 API 请求到 http://localhost:8000
- 如需修改后端地址，编辑 `frontend/vite.config.ts`
- 生产环境请修改 `SECRET_KEY` 和 `DEBUG` 配置
