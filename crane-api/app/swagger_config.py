"""Swagger 配置"""
SWAGGER_CONFIG = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec",
            "route": "/apispec.json",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/api/docs",
    "title": "Crane API 文档",
    "version": "1.0.0",
    "description": "Crane指标管理平台后端API文档",
    "termsOfService": "",
    "contact": {
        "name": "Crane API Support",
    },
    "license": {
        "name": "MIT",
    },
    "schemes": ["http", "https"],
    "basePath": "/api",
}

SWAGGER_TEMPLATE = {
    "swagger": "2.0",
    "info": {
        "title": "Crane API 文档",
        "description": "Crane指标管理平台后端API文档",
        "version": "1.0.0",
        "contact": {
            "name": "Crane API Support",
        },
    },
    "basePath": "/api",
    "schemes": ["http", "https"],
    "tags": [
        {
            "name": "数据源管理",
            "description": "数据源的增删改查和连接测试",
        },
        {
            "name": "应用管理",
            "description": "应用的管理操作",
        },
        {
            "name": "系统管理",
            "description": "用户、角色、权限管理",
        },
        {
            "name": "指标管理",
            "description": "指标的定义、监控和报表",
        },
    ],
    "definitions": {
        "ApiResponse": {
            "type": "object",
            "properties": {
                "code": {
                    "type": "integer",
                    "description": "响应状态码",
                    "example": 200,
                },
                "message": {
                    "type": "string",
                    "description": "响应消息",
                    "example": "操作成功",
                },
                "data": {
                    "type": "object",
                    "description": "响应数据",
                },
            },
        },
        "PaginatedResponse": {
            "type": "object",
            "properties": {
                "code": {
                    "type": "integer",
                    "example": 200,
                },
                "message": {
                    "type": "string",
                    "example": "查询成功",
                },
                "data": {
                    "type": "object",
                    "properties": {
                        "items": {
                            "type": "array",
                            "description": "数据列表",
                        },
                        "total": {
                            "type": "integer",
                            "description": "总记录数",
                        },
                        "page": {
                            "type": "integer",
                            "description": "当前页码",
                        },
                        "page_size": {
                            "type": "integer",
                            "description": "每页数量",
                        },
                        "pages": {
                            "type": "integer",
                            "description": "总页数",
                        },
                    },
                },
            },
        },
        "DataSource": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "integer",
                    "description": "数据源ID",
                },
                "name": {
                    "type": "string",
                    "description": "数据源名称",
                    "example": "生产环境Presto",
                },
                "type": {
                    "type": "string",
                    "enum": ["presto", "hive", "doris", "mysql"],
                    "description": "数据源类型",
                },
                "host": {
                    "type": "string",
                    "description": "主机地址",
                    "example": "localhost",
                },
                "port": {
                    "type": "integer",
                    "description": "端口",
                    "example": 8080,
                },
                "database": {
                    "type": "string",
                    "description": "数据库名称",
                },
                "catalog": {
                    "type": "string",
                    "description": "Catalog (Presto)",
                },
                "schema": {
                    "type": "string",
                    "description": "Schema",
                },
                "username": {
                    "type": "string",
                    "description": "用户名",
                },
                "password": {
                    "type": "string",
                    "description": "密码",
                },
                "config": {
                    "type": "object",
                    "description": "其他配置信息",
                },
                "status": {
                    "type": "string",
                    "enum": ["active", "inactive", "error"],
                    "description": "状态",
                },
            },
        },
    },
}

