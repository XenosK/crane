"""指标管理服务"""
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from app.models.metrics import Metric, MetricDefinition, MetricMonitoring, MetricReport
from app.extensions import db


class MetricService:
    """指标服务类"""
    
    @staticmethod
    def get_all(page: int = 1, page_size: int = 20, status: Optional[str] = None) -> Dict[str, Any]:
        """获取指标列表"""
        query = Metric.query
        
        if status:
            query = query.filter(Metric.status == status)
        
        pagination = query.order_by(Metric.created_at.desc()).paginate(
            page=page, per_page=page_size, error_out=False
        )
        
        return {
            'items': [metric.to_dict() for metric in pagination.items],
            'total': pagination.total,
            'page': page,
            'page_size': page_size,
            'pages': pagination.pages
        }
    
    @staticmethod
    def get_by_id(metric_id: int) -> Optional[Metric]:
        """根据ID获取指标"""
        return Metric.query.get(metric_id)
    
    @staticmethod
    def create(data: Dict[str, Any]) -> Metric:
        """创建指标"""
        metric = Metric(
            name=data['name'],
            code=data['code'],
            description=data.get('description'),
            type=data.get('type'),
            formula=data.get('formula'),
            unit=data.get('unit'),
            application_id=data.get('application_id'),
            status=data.get('status', 'active')
        )
        db.session.add(metric)
        db.session.commit()
        return metric
    
    @staticmethod
    def update(metric_id: int, data: Dict[str, Any]) -> Optional[Metric]:
        """更新指标"""
        metric = Metric.query.get(metric_id)
        if not metric:
            return None
        
        if 'name' in data:
            metric.name = data['name']
        if 'code' in data:
            metric.code = data['code']
        if 'description' in data:
            metric.description = data.get('description')
        if 'type' in data:
            metric.type = data.get('type')
        if 'formula' in data:
            metric.formula = data.get('formula')
        if 'unit' in data:
            metric.unit = data.get('unit')
        if 'status' in data:
            metric.status = data['status']
        
        db.session.commit()
        return metric
    
    @staticmethod
    def delete(metric_id: int) -> bool:
        """删除指标"""
        metric = Metric.query.get(metric_id)
        if not metric:
            return False
        
        db.session.delete(metric)
        db.session.commit()
        return True


class MetricDefinitionService:
    """指标定义服务类"""
    
    @staticmethod
    def get_all(page: int = 1, page_size: int = 20, metric_id: Optional[int] = None) -> Dict[str, Any]:
        """获取指标定义列表"""
        query = MetricDefinition.query
        
        if metric_id:
            query = query.filter(MetricDefinition.metric_id == metric_id)
        
        pagination = query.order_by(MetricDefinition.created_at.desc()).paginate(
            page=page, per_page=page_size, error_out=False
        )
        
        return {
            'items': [definition.to_dict() for definition in pagination.items],
            'total': pagination.total,
            'page': page,
            'page_size': page_size,
            'pages': pagination.pages
        }
    
    @staticmethod
    def create(data: Dict[str, Any]) -> MetricDefinition:
        """创建指标定义"""
        definition = MetricDefinition(
            metric_id=data['metric_id'],
            name=data['name'],
            description=data.get('description'),
            calculation_rule=data.get('calculation_rule'),
            data_source_id=data.get('data_source_id'),
            sql_query=data.get('sql_query'),
            config=data.get('config'),
            status=data.get('status', 'active')
        )
        db.session.add(definition)
        db.session.commit()
        return definition
    
    @staticmethod
    def update(definition_id: int, data: Dict[str, Any]) -> Optional[MetricDefinition]:
        """更新指标定义"""
        definition = MetricDefinition.query.get(definition_id)
        if not definition:
            return None
        
        if 'name' in data:
            definition.name = data['name']
        if 'description' in data:
            definition.description = data.get('description')
        if 'calculation_rule' in data:
            definition.calculation_rule = data.get('calculation_rule')
        if 'sql_query' in data:
            definition.sql_query = data.get('sql_query')
        if 'config' in data:
            definition.config = data.get('config')
        if 'status' in data:
            definition.status = data['status']
        
        db.session.commit()
        return definition


class MetricMonitoringService:
    """指标监控服务类"""
    
    @staticmethod
    def get_overview() -> Dict[str, Any]:
        """获取指标概览统计"""
        total_metrics = Metric.query.filter(Metric.status == 'active').count()
        active_metrics = Metric.query.filter(Metric.status == 'active').count()
        
        # 统计异常指标（最近24小时内有告警的）
        yesterday = datetime.utcnow() - timedelta(days=1)
        error_metrics = MetricMonitoring.query.filter(
            MetricMonitoring.status.in_(['warning', 'error']),
            MetricMonitoring.monitored_at >= yesterday
        ).distinct(MetricMonitoring.metric_id).count()
        
        # 今日新增指标
        today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        today_new = Metric.query.filter(Metric.created_at >= today).count()
        
        return {
            'total_metrics': total_metrics,
            'active_metrics': active_metrics,
            'error_metrics': error_metrics,
            'today_new': today_new
        }
    
    @staticmethod
    def get_monitoring_data(metric_id: int, start_time: Optional[datetime] = None, 
                           end_time: Optional[datetime] = None, limit: int = 100) -> List[Dict[str, Any]]:
        """获取监控数据"""
        query = MetricMonitoring.query.filter(MetricMonitoring.metric_id == metric_id)
        
        if start_time:
            query = query.filter(MetricMonitoring.monitored_at >= start_time)
        if end_time:
            query = query.filter(MetricMonitoring.monitored_at <= end_time)
        
        records = query.order_by(MetricMonitoring.monitored_at.desc()).limit(limit).all()
        return [record.to_dict() for record in records]
    
    @staticmethod
    def create_monitoring_record(data: Dict[str, Any]) -> MetricMonitoring:
        """创建监控记录"""
        record = MetricMonitoring(
            metric_id=data['metric_id'],
            value=data.get('value'),
            threshold_min=data.get('threshold_min'),
            threshold_max=data.get('threshold_max'),
            alert_level=data.get('alert_level'),
            status=data.get('status', 'normal'),
            monitored_at=data.get('monitored_at', datetime.utcnow())
        )
        db.session.add(record)
        db.session.commit()
        return record


class MetricReportService:
    """指标报表服务类"""
    
    @staticmethod
    def get_all(page: int = 1, page_size: int = 20) -> Dict[str, Any]:
        """获取报表列表"""
        pagination = MetricReport.query.order_by(
            MetricReport.created_at.desc()
        ).paginate(page=page, per_page=page_size, error_out=False)
        
        return {
            'items': [report.to_dict() for report in pagination.items],
            'total': pagination.total,
            'page': page,
            'page_size': page_size,
            'pages': pagination.pages
        }
    
    @staticmethod
    def create(data: Dict[str, Any]) -> MetricReport:
        """创建报表"""
        report = MetricReport(
            name=data['name'],
            description=data.get('description'),
            template=data.get('template'),
            metric_ids=data.get('metric_ids', []),
            time_range=data.get('time_range'),
            format=data.get('format', 'excel'),
            status=data.get('status', 'draft'),
            created_by=data.get('created_by')
        )
        db.session.add(report)
        db.session.commit()
        return report
    
    @staticmethod
    def generate_report(report_id: int) -> Optional[Dict[str, Any]]:
        """生成报表数据"""
        report = MetricReport.query.get(report_id)
        if not report:
            return None
        
        # 这里应该实现实际的报表生成逻辑
        # 包括查询指标数据、格式化等
        return {
            'report_id': report_id,
            'data': []  # 实际报表数据
        }

