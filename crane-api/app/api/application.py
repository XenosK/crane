"""应用管理API"""
from flask import Blueprint, request
from app.services.application_service import ApplicationService
from app.utils.response import success_response, error_response, paginated_response
from app.utils.validators import validate_required_fields

bp = Blueprint('application', __name__)


@bp.route('/list', methods=['GET'])
def get_application_list():
    """获取应用列表"""
    try:
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('page_size', 20))
        status = request.args.get('status')
        
        result = ApplicationService.get_all(page=page, page_size=page_size, status=status)
        return paginated_response(
            data=result['items'],
            total=result['total'],
            page=result['page'],
            page_size=result['page_size']
        )
    except Exception as e:
        return error_response(message=str(e), code=500)


@bp.route('/<int:app_id>', methods=['GET'])
def get_application(app_id):
    """获取应用详情"""
    try:
        application = ApplicationService.get_by_id(app_id)
        if not application:
            return error_response(message='应用不存在', code=404)
        return success_response(data=application.to_dict())
    except Exception as e:
        return error_response(message=str(e), code=500)


@bp.route('/create', methods=['POST'])
def create_application():
    """创建应用"""
    try:
        data = request.get_json()
        required_fields = ['name']
        error = validate_required_fields(data or {}, required_fields)
        if error:
            return error_response(message=error, code=400)
        
        application = ApplicationService.create(data)
        return success_response(data=application.to_dict(), message='创建成功')
    except Exception as e:
        return error_response(message=str(e), code=500)


@bp.route('/<int:app_id>', methods=['PUT'])
def update_application(app_id):
    """更新应用"""
    try:
        data = request.get_json()
        application = ApplicationService.update(app_id, data or {})
        if not application:
            return error_response(message='应用不存在', code=404)
        return success_response(data=application.to_dict(), message='更新成功')
    except Exception as e:
        return error_response(message=str(e), code=500)


@bp.route('/<int:app_id>/config', methods=['PUT'])
def update_application_config(app_id):
    """更新应用配置"""
    try:
        data = request.get_json()
        config_data = {'config': data}
        application = ApplicationService.update(app_id, config_data)
        if not application:
            return error_response(message='应用不存在', code=404)
        return success_response(data=application.to_dict(), message='配置更新成功')
    except Exception as e:
        return error_response(message=str(e), code=500)


@bp.route('/<int:app_id>', methods=['DELETE'])
def delete_application(app_id):
    """删除应用"""
    try:
        success = ApplicationService.delete(app_id)
        if not success:
            return error_response(message='应用不存在', code=404)
        return success_response(message='删除成功')
    except Exception as e:
        return error_response(message=str(e), code=500)

