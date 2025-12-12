"""指标管理模型"""
from datetime import datetime
from app.extensions import db


class Metric(db.Model):
    """指标模型"""
    __tablename__ = 'metrics'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, comment='指标名称')
    code = db.Column(db.String(100), nullable=False, unique=True, comment='指标代码')
    description = db.Column(db.Text, comment='指标描述')
    type = db.Column(db.String(50), comment='指标类型: count, sum, avg, max, min, custom')
    formula = db.Column(db.Text, comment='计算公式')
    unit = db.Column(db.String(20), comment='单位')
    application_id = db.Column(db.Integer, db.ForeignKey('applications.id'), comment='关联应用ID')
    status = db.Column(db.String(20), default='active', comment='状态: active, inactive')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'description': self.description,
            'type': self.type,
            'formula': self.formula,
            'unit': self.unit,
            'application_id': self.application_id,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
    
    def __repr__(self):
        return f'<Metric {self.name}>'


class MetricDefinition(db.Model):
    """指标定义模型"""
    __tablename__ = 'metric_definitions'
    
    id = db.Column(db.Integer, primary_key=True)
    metric_id = db.Column(db.Integer, db.ForeignKey('metrics.id'), nullable=False, comment='指标ID')
    name = db.Column(db.String(100), nullable=False, comment='定义名称')
    description = db.Column(db.Text, comment='定义描述')
    calculation_rule = db.Column(db.Text, comment='计算规则')
    data_source_id = db.Column(db.Integer, db.ForeignKey('data_sources.id'), comment='数据源ID')
    sql_query = db.Column(db.Text, comment='SQL查询语句')
    config = db.Column(db.JSON, comment='配置信息')
    status = db.Column(db.String(20), default='active', comment='状态: active, inactive')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')
    
    metric = db.relationship('Metric', backref='definitions')
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'metric_id': self.metric_id,
            'name': self.name,
            'description': self.description,
            'calculation_rule': self.calculation_rule,
            'data_source_id': self.data_source_id,
            'sql_query': self.sql_query,
            'config': self.config,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
    
    def __repr__(self):
        return f'<MetricDefinition {self.name}>'


class MetricMonitoring(db.Model):
    """指标监控模型"""
    __tablename__ = 'metric_monitoring'
    
    id = db.Column(db.Integer, primary_key=True)
    metric_id = db.Column(db.Integer, db.ForeignKey('metrics.id'), nullable=False, comment='指标ID')
    value = db.Column(db.Numeric(20, 4), comment='指标值')
    threshold_min = db.Column(db.Numeric(20, 4), comment='最小阈值')
    threshold_max = db.Column(db.Numeric(20, 4), comment='最大阈值')
    alert_level = db.Column(db.String(20), comment='告警级别: info, warning, error, critical')
    status = db.Column(db.String(20), default='normal', comment='状态: normal, warning, error')
    monitored_at = db.Column(db.DateTime, default=datetime.utcnow, comment='监控时间')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    
    metric = db.relationship('Metric', backref='monitoring_records')
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'metric_id': self.metric_id,
            'value': float(self.value) if self.value else None,
            'threshold_min': float(self.threshold_min) if self.threshold_min else None,
            'threshold_max': float(self.threshold_max) if self.threshold_max else None,
            'alert_level': self.alert_level,
            'status': self.status,
            'monitored_at': self.monitored_at.isoformat() if self.monitored_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
    
    def __repr__(self):
        return f'<MetricMonitoring {self.metric_id}>'


class MetricReport(db.Model):
    """指标报表模型"""
    __tablename__ = 'metric_reports'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, comment='报表名称')
    description = db.Column(db.Text, comment='报表描述')
    template = db.Column(db.Text, comment='报表模板')
    metric_ids = db.Column(db.JSON, comment='关联指标ID列表')
    time_range = db.Column(db.JSON, comment='时间范围')
    format = db.Column(db.String(20), default='excel', comment='导出格式: excel, pdf')
    status = db.Column(db.String(20), default='draft', comment='状态: draft, published')
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), comment='创建人ID')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')
    
    creator = db.relationship('User', backref='reports')
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'template': self.template,
            'metric_ids': self.metric_ids,
            'time_range': self.time_range,
            'format': self.format,
            'status': self.status,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
    
    def __repr__(self):
        return f'<MetricReport {self.name}>'

