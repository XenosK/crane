"""测试配置"""
import pytest
from app import create_app
from app.config import TestingConfig
from app.extensions import db


@pytest.fixture
def app():
    """创建测试应用"""
    app = create_app(TestingConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    """测试客户端"""
    return app.test_client()


@pytest.fixture
def runner(app):
    """测试运行器"""
    return app.test_cli_runner()

