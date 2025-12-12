"""数据源管理API"""
from flask import Blueprint, request
from app.services.datasource_service import DataSourceService
from app.utils.response import success_response, error_response, paginated_response
from app.utils.validators import validate_required_fields

bp = Blueprint('datasource', __name__)


@bp.route('/list', methods=['GET'])
def get_datasource_list():
    """获取数据源列表"""
    try:
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('page_size', 20))
        type = request.args.get('type')
        
        result = DataSourceService.get_all(page=page, page_size=page_size, type=type)
        return paginated_response(
            data=result['items'],
            total=result['total'],
            page=result['page'],
            page_size=result['page_size']
        )
    except Exception as e:
        return error_response(message=str(e), code=500)


@bp.route('/<int:ds_id>', methods=['GET'])
def get_datasource(ds_id):
    """获取数据源详情"""
    try:
        data_source = DataSourceService.get_by_id(ds_id)
        if not data_source:
            return error_response(message='数据源不存在', code=404)
        return success_response(data=data_source.to_dict())
    except Exception as e:
        return error_response(message=str(e), code=500)


@bp.route('/type/<string:ds_type>', methods=['GET'])
def get_datasource_by_type(ds_type):
    """根据类型获取数据源列表"""
    try:
        data_sources = DataSourceService.get_by_type(ds_type)
        return success_response(data=[ds.to_dict() for ds in data_sources])
    except Exception as e:
        return error_response(message=str(e), code=500)


@bp.route('/create', methods=['POST'])
def create_datasource():
    """创建数据源"""
    try:
        data = request.get_json()
        required_fields = ['name', 'type', 'host', 'port']
        error = validate_required_fields(data or {}, required_fields)
        if error:
            return error_response(message=error, code=400)
        
        data_source = DataSourceService.create(data)
        return success_response(data=data_source.to_dict(), message='创建成功')
    except ValueError as e:
        return error_response(message=str(e), code=400)
    except Exception as e:
        return error_response(message=str(e), code=500)


@bp.route('/<int:ds_id>', methods=['PUT'])
def update_datasource(ds_id):
    """更新数据源"""
    try:
        data = request.get_json()
        data_source = DataSourceService.update(ds_id, data or {})
        if not data_source:
            return error_response(message='数据源不存在', code=404)
        return success_response(data=data_source.to_dict(), message='更新成功')
    except ValueError as e:
        return error_response(message=str(e), code=400)
    except Exception as e:
        return error_response(message=str(e), code=500)


@bp.route('/<int:ds_id>/test', methods=['POST'])
def test_datasource_connection(ds_id):
    """测试数据源连接"""
    try:
        result = DataSourceService.test_connection(ds_id)
        if result['success']:
            return success_response(data=result, message='连接测试成功')
        else:
            return error_response(message=result['message'], code=400)
    except Exception as e:
        return error_response(message=str(e), code=500)


@bp.route('/<int:ds_id>', methods=['DELETE'])
def delete_datasource(ds_id):
    """删除数据源"""
    try:
        success = DataSourceService.delete(ds_id)
        if not success:
            return error_response(message='数据源不存在', code=404)
        return success_response(message='删除成功')
    except Exception as e:
        return error_response(message=str(e), code=500)

