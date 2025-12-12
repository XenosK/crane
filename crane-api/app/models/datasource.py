"""数据源模型"""
from datetime import datetime
from app.extensions import db


class DataSource(db.Model):
    """数据源模型"""
    __tablename__ = 'data_sources'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True, comment='数据源名称')
    type = db.Column(db.String(50), nullable=False, comment='数据源类型: presto, hive, doris, mysql')
    host = db.Column(db.String(100), nullable=False, comment='主机地址')
    port = db.Column(db.Integer, nullable=False, comment='端口')
    database = db.Column(db.String(100), comment='数据库名称')
    catalog = db.Column(db.String(100), comment='Catalog (Presto)')
    schema = db.Column(db.String(100), comment='Schema')
    username = db.Column(db.String(100), comment='用户名')
    password = db.Column(db.String(255), comment='密码(加密存储)')
    config = db.Column(db.JSON, comment='其他配置信息')
    status = db.Column(db.String(20), default='active', comment='状态: active, inactive, error')
    last_test_at = db.Column(db.DateTime, comment='最后测试时间')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')
    
    def to_dict(self, include_password=False):
        """转换为字典"""
        data = {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'host': self.host,
            'port': self.port,
            'database': self.database,
            'catalog': self.catalog,
            'schema': self.schema,
            'username': self.username,
            'config': self.config,
            'status': self.status,
            'last_test_at': self.last_test_at.isoformat() if self.last_test_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
        if include_password:
            data['password'] = self.password
        return data
    
    def __repr__(self):
        return f'<DataSource {self.name}>'

