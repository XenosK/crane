# 项目结构说明

## 目录结构

```
crane-api/
├── app/                          # 应用主目录
│   ├── __init__.py              # Flask应用工厂，初始化应用和注册蓝图
│   ├── config.py                # 配置文件（开发/生产/测试环境）
│   ├── extensions.py            # Flask扩展初始化（db, migrate, jwt）
│   │
│   ├── api/                     # API路由层
│   │   ├── __init__.py
│   │   ├── application.py       # 应用管理API路由
│   │   ├── system.py            # 系统管理API路由（用户/角色/权限）
│   │   ├── metrics.py           # 指标管理API路由
│   │   └── datasource.py        # 数据源管理API路由
│   │
│   ├── models/                   # 数据模型层
│   │   ├── __init__.py
│   │   ├── application.py       # Application模型
│   │   ├── system.py            # User, Role, Permission模型
│   │   ├── metrics.py           # Metric, MetricDefinition, MetricMonitoring, MetricReport模型
│   │   └── datasource.py        # DataSource模型
│   │
│   ├── services/                 # 业务逻辑服务层
│   │   ├── __init__.py
│   │   ├── application_service.py    # 应用管理服务
│   │   ├── system_service.py         # 系统管理服务（UserService, RoleService, PermissionService）
│   │   ├── metrics_service.py        # 指标管理服务（MetricService, MetricDefinitionService等）
│   │   └── datasource_service.py     # 数据源管理服务
│   │
│   └── utils/                    # 工具函数
│       ├── __init__.py
│       ├── response.py          # 统一响应格式（success_response, error_response, paginated_response）
│       └── validators.py        # 数据验证工具
│
├── migrations/                   # 数据库迁移文件（Flask-Migrate）
│   └── README.md
│
├── tests/                        # 测试文件
│   ├── __init__.py
│   └── conftest.py              # pytest配置和fixtures
│
├── run.py                        # 应用启动入口
├── pyproject.toml               # 项目依赖配置
├── .gitignore                   # Git忽略文件
├── .env.example                 # 环境变量示例
├── README.md                     # 项目说明文档
└── PROJECT_STRUCTURE.md         # 项目结构说明（本文件）
```

## 模块对应关系

### 前端页面 → 后端API映射

| 前端页面 | 后端API模块 | 主要功能 |
|---------|------------|---------|
| ApplicationList | `app/api/application.py` | 应用列表查询 |
| ApplicationCreate | `app/api/application.py` | 应用创建 |
| ApplicationConfig | `app/api/application.py` | 应用配置管理 |
| SystemUser | `app/api/system.py` | 用户管理 |
| SystemRole | `app/api/system.py` | 角色管理 |
| SystemPermission | `app/api/system.py` | 权限管理 |
| DataSourceList | `app/api/datasource.py` | 数据源列表 |
| DataSourceConfigModal | `app/api/datasource.py` | 数据源配置 |
| MetricsOverview | `app/api/metrics.py` | 指标概览统计 |
| MetricsDefinition | `app/api/metrics.py` | 指标定义管理 |
| MetricsMonitoring | `app/api/metrics.py` | 指标监控 |
| MetricsReport | `app/api/metrics.py` | 指标报表 |

## 架构设计

### 分层架构

```
┌─────────────────────────────────┐
│      API Layer (路由层)          │
│   - 请求处理                      │
│   - 参数验证                      │
│   - 响应格式化                    │
└──────────────┬──────────────────┘
               │
┌──────────────▼──────────────────┐
│    Service Layer (服务层)        │
│   - 业务逻辑处理                  │
│   - 数据组装                     │
│   - 事务管理                     │
└──────────────┬──────────────────┘
               │
┌──────────────▼──────────────────┐
│     Model Layer (模型层)         │
│   - 数据模型定义                  │
│   - 数据库操作                    │
│   - 关系映射                     │
└─────────────────────────────────┘
```

### 数据流

1. **请求流程**: 客户端 → API路由 → 服务层 → 模型层 → 数据库
2. **响应流程**: 数据库 → 模型层 → 服务层 → API路由 → 客户端

## 核心设计原则

1. **单一职责**: 每个模块只负责一个功能领域
2. **分层清晰**: API层、服务层、模型层职责明确
3. **可扩展性**: 易于添加新功能和模块
4. **可维护性**: 代码结构清晰，易于理解和修改
5. **可测试性**: 服务层可独立测试，不依赖HTTP层

## 数据库设计

### 主要数据表

- `applications` - 应用表
- `users` - 用户表
- `roles` - 角色表
- `permissions` - 权限表
- `user_role` - 用户角色关联表
- `role_permission` - 角色权限关联表
- `metrics` - 指标表
- `metric_definitions` - 指标定义表
- `metric_monitoring` - 指标监控表
- `metric_reports` - 指标报表表
- `data_sources` - 数据源表

## 扩展建议

1. **认证授权**: 集成JWT认证，添加权限中间件
2. **日志系统**: 添加日志记录和监控
3. **缓存**: 使用Redis缓存热点数据
4. **消息队列**: 异步任务处理（如报表生成）
5. **API文档**: 集成Swagger/OpenAPI文档
6. **单元测试**: 完善测试覆盖
7. **CI/CD**: 添加持续集成和部署流程

