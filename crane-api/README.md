# Crane API

Crane指标管理平台后端API服务，基于Flask框架开发。

## 项目结构

```
crane-api/
├── app/                    # 应用主目录
│   ├── __init__.py        # Flask应用工厂
│   ├── config.py          # 配置文件
│   ├── extensions.py      # Flask扩展初始化
│   ├── api/               # API路由模块
│   │   ├── application.py # 应用管理API
│   │   ├── system.py      # 系统管理API（用户、角色、权限）
│   │   ├── metrics.py     # 指标管理API
│   │   └── datasource.py  # 数据源管理API
│   ├── models/            # 数据模型
│   │   ├── application.py # 应用模型
│   │   ├── system.py      # 系统模型（用户、角色、权限）
│   │   ├── metrics.py     # 指标模型
│   │   └── datasource.py  # 数据源模型
│   ├── services/          # 业务逻辑层
│   │   ├── application_service.py
│   │   ├── system_service.py
│   │   ├── metrics_service.py
│   │   └── datasource_service.py
│   └── utils/             # 工具函数
│       ├── response.py    # 统一响应格式
│       └── validators.py  # 数据验证
├── migrations/            # 数据库迁移文件
├── tests/                 # 测试文件
├── run.py                 # 应用启动文件
├── pyproject.toml         # 项目依赖配置
└── README.md              # 项目说明文档
```

## 功能模块

### 1. 应用管理 (Application)
- 应用列表查询
- 应用创建
- 应用配置管理
- 应用更新和删除

### 2. 系统管理 (System)
- **用户管理**: 用户CRUD、角色分配
- **角色管理**: 角色CRUD、权限分配
- **权限管理**: 权限CRUD、权限树结构
- **数据源管理**: 支持Presto、Hive、Doris、MySQL等数据源配置

### 3. 指标管理 (Metrics)
- **指标概览**: 统计指标总数、活跃指标、异常指标等
- **指标定义**: 指标CRUD、计算公式配置
- **指标监控**: 实时监控数据、告警管理
- **指标报表**: 报表创建、生成和导出

## 技术栈

- **框架**: Flask 3.1+
- **ORM**: SQLAlchemy
- **数据库迁移**: Flask-Migrate
- **认证**: Flask-JWT-Extended
- **跨域**: Flask-CORS

## 快速开始

### 1. 安装依赖

```bash
# 使用uv（推荐）
uv sync

# 或使用pip
pip install -r requirements.txt
```

### 2. 配置环境变量

复制 `.env.example` 为 `.env` 并修改配置：

```bash
cp .env.example .env
```

### 3. 初始化数据库

```bash
# 初始化迁移
flask db init

# 创建迁移
flask db migrate -m "Initial migration"

# 应用迁移
flask db upgrade
```

### 4. 启动应用

```bash
python run.py
```

应用将在 `http://localhost:5000` 启动。

## API接口

### 应用管理
- `GET /api/application/list` - 获取应用列表
- `GET /api/application/<id>` - 获取应用详情
- `POST /api/application/create` - 创建应用
- `PUT /api/application/<id>` - 更新应用
- `PUT /api/application/<id>/config` - 更新应用配置
- `DELETE /api/application/<id>` - 删除应用

### 系统管理
- `GET /api/system/user/list` - 获取用户列表
- `POST /api/system/user/create` - 创建用户
- `PUT /api/system/user/<id>/roles` - 分配用户角色
- `GET /api/system/role/list` - 获取角色列表
- `PUT /api/system/role/<id>/permissions` - 分配角色权限
- `GET /api/system/permission/list` - 获取权限列表

### 指标管理
- `GET /api/metrics/overview` - 获取指标概览
- `GET /api/metrics/list` - 获取指标列表
- `POST /api/metrics/create` - 创建指标
- `GET /api/metrics/definition/list` - 获取指标定义列表
- `GET /api/metrics/monitoring/<id>` - 获取监控数据
- `GET /api/metrics/report/list` - 获取报表列表

### 数据源管理
- `GET /api/datasource/list` - 获取数据源列表
- `POST /api/datasource/create` - 创建数据源
- `POST /api/datasource/<id>/test` - 测试数据源连接
- `PUT /api/datasource/<id>` - 更新数据源
- `DELETE /api/datasource/<id>` - 删除数据源

## 开发规范

### 代码结构
- **API层** (`app/api/`): 处理HTTP请求，参数验证，调用服务层
- **服务层** (`app/services/`): 业务逻辑处理
- **模型层** (`app/models/`): 数据模型定义
- **工具层** (`app/utils/`): 通用工具函数

### 响应格式
所有API统一使用以下响应格式：

```json
{
  "code": 200,
  "message": "操作成功",
  "data": {}
}
```

### 分页响应
```json
{
  "code": 200,
  "message": "查询成功",
  "data": {
    "items": [],
    "total": 100,
    "page": 1,
    "page_size": 20,
    "pages": 5
  }
}
```

## 测试

```bash
# 运行测试
pytest

# 带覆盖率
pytest --cov=app
```

## 部署

### 生产环境配置

1. 设置环境变量：
   - `FLASK_ENV=production`
   - `SECRET_KEY`: 生成强密钥
   - `DATABASE_URL`: 生产数据库连接
   - `CORS_ORIGINS`: 允许的前端域名

2. 使用生产级WSGI服务器（如Gunicorn）：
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 run:app
   ```

## 许可证

MIT License

