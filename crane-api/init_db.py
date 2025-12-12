#!/usr/bin/env python
"""
数据库初始化脚本
用于创建数据库表结构
"""
import os
import sys

# 设置环境变量
os.environ.setdefault('FLASK_ENV', 'development')

from app import create_app
from app.config import config
from app.extensions import db
from app.models import (
    Application,
    User, Role, Permission,
    Metric, MetricDefinition, MetricMonitoring, MetricReport,
    DataSource
)

def init_database():
    """初始化数据库"""
    app = create_app(config.get(os.environ.get('FLASK_ENV', 'development')))
    
    with app.app_context():
        print("正在创建数据库表...")
        try:
            # 创建所有表
            db.create_all()
            print("✓ 数据库表创建成功！")
            print("\n已创建的表：")
            print("  - data_sources (数据源)")
            print("  - applications (应用)")
            print("  - users, roles, permissions (用户、角色、权限)")
            print("  - metrics, metric_definitions, metric_monitoring, metric_reports (指标相关)")
        except Exception as e:
            print(f"✗ 创建数据库表时出错: {e}")
            sys.exit(1)

if __name__ == '__main__':
    init_database()

