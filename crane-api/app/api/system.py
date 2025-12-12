"""系统管理API"""
from flask import Blueprint, request
from app.services.system_service import UserService, RoleService, PermissionService
from app.utils.response import success_response, error_response, paginated_response
from app.utils.validators import validate_required_fields

bp = Blueprint('system', __name__)


# ============ 用户管理 ============
@bp.route('/user/list', methods=['GET'])
def get_user_list():
    """获取用户列表"""
    try:
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('page_size', 20))
        status = request.args.get('status')
        
        result = UserService.get_all(page=page, page_size=page_size, status=status)
        return paginated_response(
            data=result['items'],
            total=result['total'],
            page=result['page'],
            page_size=result['page_size']
        )
    except Exception as e:
        return error_response(message=str(e), code=500)


@bp.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """获取用户详情"""
    try:
        user = UserService.get_by_id(user_id)
        if not user:
            return error_response(message='用户不存在', code=404)
        return success_response(data=user.to_dict(include_roles=True))
    except Exception as e:
        return error_response(message=str(e), code=500)


@bp.route('/user/create', methods=['POST'])
def create_user():
    """创建用户"""
    try:
        data = request.get_json()
        required_fields = ['username', 'password']
        error = validate_required_fields(data or {}, required_fields)
        if error:
            return error_response(message=error, code=400)
        
        user = UserService.create(data)
        return success_response(data=user.to_dict(), message='创建成功')
    except Exception as e:
        return error_response(message=str(e), code=500)


@bp.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """更新用户"""
    try:
        data = request.get_json()
        user = UserService.update(user_id, data or {})
        if not user:
            return error_response(message='用户不存在', code=404)
        return success_response(data=user.to_dict(), message='更新成功')
    except Exception as e:
        return error_response(message=str(e), code=500)


@bp.route('/user/<int:user_id>/roles', methods=['PUT'])
def assign_user_roles(user_id):
    """分配用户角色"""
    try:
        data = request.get_json()
        role_ids = data.get('role_ids', [])
        user = UserService.assign_roles(user_id, role_ids)
        if not user:
            return error_response(message='用户不存在', code=404)
        return success_response(data=user.to_dict(include_roles=True), message='角色分配成功')
    except Exception as e:
        return error_response(message=str(e), code=500)


@bp.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """删除用户"""
    try:
        success = UserService.delete(user_id)
        if not success:
            return error_response(message='用户不存在', code=404)
        return success_response(message='删除成功')
    except Exception as e:
        return error_response(message=str(e), code=500)


# ============ 角色管理 ============
@bp.route('/role/list', methods=['GET'])
def get_role_list():
    """获取角色列表"""
    try:
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('page_size', 20))
        status = request.args.get('status')
        
        result = RoleService.get_all(page=page, page_size=page_size, status=status)
        return paginated_response(
            data=result['items'],
            total=result['total'],
            page=result['page'],
            page_size=result['page_size']
        )
    except Exception as e:
        return error_response(message=str(e), code=500)


@bp.route('/role/<int:role_id>', methods=['GET'])
def get_role(role_id):
    """获取角色详情"""
    try:
        role = RoleService.get_by_id(role_id)
        if not role:
            return error_response(message='角色不存在', code=404)
        return success_response(data=role.to_dict(include_permissions=True))
    except Exception as e:
        return error_response(message=str(e), code=500)


@bp.route('/role/create', methods=['POST'])
def create_role():
    """创建角色"""
    try:
        data = request.get_json()
        required_fields = ['name', 'code']
        error = validate_required_fields(data or {}, required_fields)
        if error:
            return error_response(message=error, code=400)
        
        role = RoleService.create(data)
        return success_response(data=role.to_dict(), message='创建成功')
    except Exception as e:
        return error_response(message=str(e), code=500)


@bp.route('/role/<int:role_id>', methods=['PUT'])
def update_role(role_id):
    """更新角色"""
    try:
        data = request.get_json()
        role = RoleService.update(role_id, data or {})
        if not role:
            return error_response(message='角色不存在', code=404)
        return success_response(data=role.to_dict(), message='更新成功')
    except Exception as e:
        return error_response(message=str(e), code=500)


@bp.route('/role/<int:role_id>/permissions', methods=['PUT'])
def assign_role_permissions(role_id):
    """分配角色权限"""
    try:
        data = request.get_json()
        permission_ids = data.get('permission_ids', [])
        role = RoleService.assign_permissions(role_id, permission_ids)
        if not role:
            return error_response(message='角色不存在', code=404)
        return success_response(data=role.to_dict(include_permissions=True), message='权限分配成功')
    except Exception as e:
        return error_response(message=str(e), code=500)


@bp.route('/role/<int:role_id>', methods=['DELETE'])
def delete_role(role_id):
    """删除角色"""
    try:
        success = RoleService.delete(role_id)
        if not success:
            return error_response(message='角色不存在', code=404)
        return success_response(message='删除成功')
    except Exception as e:
        return error_response(message=str(e), code=500)


# ============ 权限管理 ============
@bp.route('/permission/list', methods=['GET'])
def get_permission_list():
    """获取权限列表"""
    try:
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('page_size', 20))
        resource = request.args.get('resource')
        
        result = PermissionService.get_all(page=page, page_size=page_size, resource=resource)
        return paginated_response(
            data=result['items'],
            total=result['total'],
            page=result['page'],
            page_size=result['page_size']
        )
    except Exception as e:
        return error_response(message=str(e), code=500)


@bp.route('/permission/<int:permission_id>', methods=['GET'])
def get_permission(permission_id):
    """获取权限详情"""
    try:
        permission = PermissionService.get_by_id(permission_id)
        if not permission:
            return error_response(message='权限不存在', code=404)
        return success_response(data=permission.to_dict(include_children=True))
    except Exception as e:
        return error_response(message=str(e), code=500)


@bp.route('/permission/create', methods=['POST'])
def create_permission():
    """创建权限"""
    try:
        data = request.get_json()
        required_fields = ['name', 'code']
        error = validate_required_fields(data or {}, required_fields)
        if error:
            return error_response(message=error, code=400)
        
        permission = PermissionService.create(data)
        return success_response(data=permission.to_dict(), message='创建成功')
    except Exception as e:
        return error_response(message=str(e), code=500)


@bp.route('/permission/<int:permission_id>', methods=['PUT'])
def update_permission(permission_id):
    """更新权限"""
    try:
        data = request.get_json()
        permission = PermissionService.update(permission_id, data or {})
        if not permission:
            return error_response(message='权限不存在', code=404)
        return success_response(data=permission.to_dict(), message='更新成功')
    except Exception as e:
        return error_response(message=str(e), code=500)


@bp.route('/permission/<int:permission_id>', methods=['DELETE'])
def delete_permission(permission_id):
    """删除权限"""
    try:
        success = PermissionService.delete(permission_id)
        if not success:
            return error_response(message='权限不存在', code=404)
        return success_response(message='删除成功')
    except Exception as e:
        return error_response(message=str(e), code=500)

