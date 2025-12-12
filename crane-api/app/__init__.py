"""Flask应用工厂"""
from flask import Flask
from flask_cors import CORS
from flasgger import Swagger
from app.config import Config
from app.extensions import db, migrate, jwt
from app.swagger_config import SWAGGER_CONFIG, SWAGGER_TEMPLATE


def create_app(config_class=Config):
    """应用工厂函数"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # 初始化扩展
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app)
    
    # 初始化 Swagger
    Swagger(app, config=SWAGGER_CONFIG, template=SWAGGER_TEMPLATE)
    
    # 导入所有模型，确保 Flask-Migrate 能检测到它们
    from app.models import (
        Application,
        User, Role, Permission,
        Metric, MetricDefinition, MetricMonitoring, MetricReport,
        DataSource
    )
    
    # 注册蓝图
    from app.api import auth, application, system, metrics, datasource
    app.register_blueprint(auth.bp, url_prefix='/api/auth')
    app.register_blueprint(application.bp, url_prefix='/api/application')
    app.register_blueprint(system.bp, url_prefix='/api/system')
    app.register_blueprint(metrics.bp, url_prefix='/api/metrics')
    app.register_blueprint(datasource.bp, url_prefix='/api/datasource')
    
    return app

