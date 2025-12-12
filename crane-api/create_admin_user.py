#!/usr/bin/env python
"""
创建默认管理员用户脚本
"""
import os
import sys

# 设置环境变量
os.environ.setdefault('FLASK_ENV', 'development')

from app import create_app
from app.config import config
from app.extensions import db
from app.models.system import User

def create_admin_user():
    """创建默认管理员用户"""
    app = create_app(config.get(os.environ.get('FLASK_ENV', 'development')))
    
    with app.app_context():
        # 检查是否已存在 admin 用户
        admin_user = User.query.filter_by(username='admin').first()
        if admin_user:
            print("✓ 管理员用户已存在，跳过创建")
            print(f"  用户名: {admin_user.username}")
            return
        
        # 创建默认管理员用户
        admin_user = User(
            username='admin',
            email='admin@crane.com',
            real_name='系统管理员',
            status='active'
        )
        admin_user.set_password('admin123')  # 默认密码
        
        db.session.add(admin_user)
        db.session.commit()
        
        print("✓ 默认管理员用户创建成功！")
        print(f"  用户名: admin")
        print(f"  密码: admin123")
        print("  请登录后及时修改密码！")

if __name__ == '__main__':
    create_admin_user()

