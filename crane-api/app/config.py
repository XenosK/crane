"""应用配置"""
import os
from datetime import timedelta
from urllib.parse import quote_plus


def get_database_uri():
    """
    根据配置获取数据库 URI
    支持 SQLite（默认）和 MySQL
    通过环境变量配置：
    - DB_TYPE: 数据库类型，可选 'sqlite' 或 'mysql'，默认为 'sqlite'
    - DATABASE_URL: 完整的数据库连接字符串（优先级最高）
    
    MySQL 配置项：
    - DB_HOST: MySQL 主机地址，默认 'localhost'
    - DB_PORT: MySQL 端口，默认 3306
    - DB_USER: MySQL 用户名，默认 'root'
    - DB_PASSWORD: MySQL 密码
    - DB_NAME: MySQL 数据库名，默认 'crane'
    - DB_CHARSET: MySQL 字符集，默认 'utf8mb4'
    
    SQLite 配置项：
    - DB_PATH: SQLite 数据库文件路径，默认 'crane.db'
    """
    # 如果设置了完整的 DATABASE_URL，直接使用
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        return database_url
    
    # 获取数据库类型，默认为 sqlite
    db_type = os.environ.get('DB_TYPE', 'sqlite').lower()
    
    if db_type == 'mysql':
        # MySQL 配置
        db_host = os.environ.get('DB_HOST', 'localhost')
        db_port = os.environ.get('DB_PORT', '3306')
        db_user = os.environ.get('DB_USER', 'root')
        db_password = os.environ.get('DB_PASSWORD', '')
        db_name = os.environ.get('DB_NAME', 'crane')
        db_charset = os.environ.get('DB_CHARSET', 'utf8mb4')
        
        # 构建 MySQL URI
        if db_password:
            # 对密码进行 URL 编码，防止特殊字符导致连接失败
            encoded_password = quote_plus(db_password)
            uri = f'mysql+pymysql://{db_user}:{encoded_password}@{db_host}:{db_port}/{db_name}?charset={db_charset}'
        else:
            uri = f'mysql+pymysql://{db_user}@{db_host}:{db_port}/{db_name}?charset={db_charset}'
        
        return uri
    else:
        # SQLite 配置（默认）
        db_path = os.environ.get('DB_PATH', 'crane.db')
        # 如果路径不是绝对路径，使用相对路径
        if not os.path.isabs(db_path):
            # 确保路径相对于项目根目录
            return f'sqlite:///{db_path}'
        else:
            return f'sqlite:///{db_path}'


class Config:
    """基础配置"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = get_database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    
    # JWT配置
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key-change-in-production'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    # CORS配置
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*').split(',')
    
    # 分页配置
    ITEMS_PER_PAGE = 20


class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False


class TestingConfig(Config):
    """测试环境配置"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

