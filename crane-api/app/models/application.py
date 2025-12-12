"""应用管理模型"""
from datetime import datetime
from app.extensions import db


class Application(db.Model):
    """应用模型"""
    __tablename__ = 'applications'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True, comment='应用名称')
    description = db.Column(db.Text, comment='应用描述')
    owner = db.Column(db.String(50), comment='负责人')
    status = db.Column(db.String(20), default='active', comment='状态: active, inactive')
    config = db.Column(db.JSON, comment='应用配置')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')
    
    # 关联指标
    metrics = db.relationship('Metric', backref='application', lazy='dynamic', cascade='all, delete-orphan')
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'owner': self.owner,
            'status': self.status,
            'config': self.config,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'metrics_count': self.metrics.count()
        }
    
    def __repr__(self):
        return f'<Application {self.name}>'

