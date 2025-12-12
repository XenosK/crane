"""指标管理API"""
from flask import Blueprint, request
from datetime import datetime
from app.services.metrics_service import (
    MetricService, MetricDefinitionService, 
    MetricMonitoringService, MetricReportService
)
from app.utils.response import success_response, error_response, paginated_response
from app.utils.validators import validate_required_fields

bp = Blueprint('metrics', __name__)


# ============ 指标概览 ============
@bp.route('/overview', methods=['GET'])
def get_metrics_overview():
    """获取指标概览统计"""
    try:
        overview = MetricMonitoringService.get_overview()
        return success_response(data=overview)
    except Exception as e:
        return error_response(message=str(e), code=500)


# ============ 指标定义 ============
@bp.route('/list', methods=['GET'])
def get_metric_list():
    """获取指标列表"""
    try:
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('page_size', 20))
        status = request.args.get('status')
        
        result = MetricService.get_all(page=page, page_size=page_size, status=status)
        return paginated_response(
            data=result['items'],
            total=result['total'],
            page=result['page'],
            page_size=result['page_size']
        )
    except Exception as e:
        return error_response(message=str(e), code=500)


@bp.route('/<int:metric_id>', methods=['GET'])
def get_metric(metric_id):
    """获取指标详情"""
    try:
        metric = MetricService.get_by_id(metric_id)
        if not metric:
            return error_response(message='指标不存在', code=404)
        return success_response(data=metric.to_dict())
    except Exception as e:
        return error_response(message=str(e), code=500)


@bp.route('/create', methods=['POST'])
def create_metric():
    """创建指标"""
    try:
        data = request.get_json()
        required_fields = ['name', 'code']
        error = validate_required_fields(data or {}, required_fields)
        if error:
            return error_response(message=error, code=400)
        
        metric = MetricService.create(data)
        return success_response(data=metric.to_dict(), message='创建成功')
    except Exception as e:
        return error_response(message=str(e), code=500)


@bp.route('/<int:metric_id>', methods=['PUT'])
def update_metric(metric_id):
    """更新指标"""
    try:
        data = request.get_json()
        metric = MetricService.update(metric_id, data or {})
        if not metric:
            return error_response(message='指标不存在', code=404)
        return success_response(data=metric.to_dict(), message='更新成功')
    except Exception as e:
        return error_response(message=str(e), code=500)


@bp.route('/<int:metric_id>', methods=['DELETE'])
def delete_metric(metric_id):
    """删除指标"""
    try:
        success = MetricService.delete(metric_id)
        if not success:
            return error_response(message='指标不存在', code=404)
        return success_response(message='删除成功')
    except Exception as e:
        return error_response(message=str(e), code=500)


# ============ 指标定义 ============
@bp.route('/definition/list', methods=['GET'])
def get_definition_list():
    """获取指标定义列表"""
    try:
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('page_size', 20))
        metric_id = request.args.get('metric_id', type=int)
        
        result = MetricDefinitionService.get_all(
            page=page, page_size=page_size, metric_id=metric_id
        )
        return paginated_response(
            data=result['items'],
            total=result['total'],
            page=result['page'],
            page_size=result['page_size']
        )
    except Exception as e:
        return error_response(message=str(e), code=500)


@bp.route('/definition/create', methods=['POST'])
def create_definition():
    """创建指标定义"""
    try:
        data = request.get_json()
        required_fields = ['metric_id', 'name']
        error = validate_required_fields(data or {}, required_fields)
        if error:
            return error_response(message=error, code=400)
        
        definition = MetricDefinitionService.create(data)
        return success_response(data=definition.to_dict(), message='创建成功')
    except Exception as e:
        return error_response(message=str(e), code=500)


@bp.route('/definition/<int:definition_id>', methods=['PUT'])
def update_definition(definition_id):
    """更新指标定义"""
    try:
        data = request.get_json()
        definition = MetricDefinitionService.update(definition_id, data or {})
        if not definition:
            return error_response(message='指标定义不存在', code=404)
        return success_response(data=definition.to_dict(), message='更新成功')
    except Exception as e:
        return error_response(message=str(e), code=500)


# ============ 指标监控 ============
@bp.route('/monitoring/<int:metric_id>', methods=['GET'])
def get_monitoring_data(metric_id):
    """获取指标监控数据"""
    try:
        start_time_str = request.args.get('start_time')
        end_time_str = request.args.get('end_time')
        limit = int(request.args.get('limit', 100))
        
        start_time = datetime.fromisoformat(start_time_str) if start_time_str else None
        end_time = datetime.fromisoformat(end_time_str) if end_time_str else None
        
        data = MetricMonitoringService.get_monitoring_data(
            metric_id, start_time=start_time, end_time=end_time, limit=limit
        )
        return success_response(data=data)
    except Exception as e:
        return error_response(message=str(e), code=500)


@bp.route('/monitoring/create', methods=['POST'])
def create_monitoring_record():
    """创建监控记录"""
    try:
        data = request.get_json()
        required_fields = ['metric_id']
        error = validate_required_fields(data or {}, required_fields)
        if error:
            return error_response(message=error, code=400)
        
        record = MetricMonitoringService.create_monitoring_record(data)
        return success_response(data=record.to_dict(), message='创建成功')
    except Exception as e:
        return error_response(message=str(e), code=500)


# ============ 指标报表 ============
@bp.route('/report/list', methods=['GET'])
def get_report_list():
    """获取报表列表"""
    try:
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('page_size', 20))
        
        result = MetricReportService.get_all(page=page, page_size=page_size)
        return paginated_response(
            data=result['items'],
            total=result['total'],
            page=result['page'],
            page_size=result['page_size']
        )
    except Exception as e:
        return error_response(message=str(e), code=500)


@bp.route('/report/create', methods=['POST'])
def create_report():
    """创建报表"""
    try:
        data = request.get_json()
        required_fields = ['name']
        error = validate_required_fields(data or {}, required_fields)
        if error:
            return error_response(message=error, code=400)
        
        report = MetricReportService.create(data)
        return success_response(data=report.to_dict(), message='创建成功')
    except Exception as e:
        return error_response(message=str(e), code=500)


@bp.route('/report/<int:report_id>/generate', methods=['POST'])
def generate_report(report_id):
    """生成报表"""
    try:
        result = MetricReportService.generate_report(report_id)
        if not result:
            return error_response(message='报表不存在', code=404)
        return success_response(data=result, message='报表生成成功')
    except Exception as e:
        return error_response(message=str(e), code=500)

