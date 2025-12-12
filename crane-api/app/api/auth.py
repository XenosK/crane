"""认证API"""
from flask import Blueprint, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import datetime
from app.services.system_service import UserService
from app.utils.response import success_response, error_response

bp = Blueprint('auth', __name__)


@bp.route('/login', methods=['POST'])
def login():
    """
    用户登录
    ---
    tags:
      - 认证
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - username
            - password
          properties:
            username:
              type: string
              description: 用户名
              example: admin
            password:
              type: string
              description: 密码
              example: admin123
    responses:
      200:
        description: 登录成功
        schema:
          $ref: '#/definitions/ApiResponse'
      401:
        description: 用户名或密码错误
        schema:
          $ref: '#/definitions/ApiResponse'
    """
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return error_response(message='用户名和密码不能为空', code=400)
        
        # 查找用户
        user = UserService.get_by_username(username)
        if not user:
            # 添加调试信息：检查数据库中是否有任何用户
            from app.models.system import User
            user_count = User.query.count()
            if user_count == 0:
                return error_response(
                    message='用户不存在。请先运行 create_admin_user.py 创建默认管理员用户', 
                    code=401
                )
            return error_response(message='用户名或密码错误', code=401)
        
        # 验证密码
        if not user.check_password(password):
            return error_response(message='用户名或密码错误', code=401)
        
        # 检查用户状态
        if user.status != 'active':
            return error_response(message='用户已被禁用', code=403)
        
        # 更新最后登录时间
        user.last_login = datetime.utcnow()
        from app.extensions import db
        db.session.commit()
        
        # 生成 JWT token
        access_token = create_access_token(identity=user.id)
        
        return success_response(
            data={
                'token': access_token,
                'user': user.to_dict(include_roles=True)
            },
            message='登录成功'
        )
    except Exception as e:
        return error_response(message=str(e), code=500)


@bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """
    获取当前用户信息
    ---
    tags:
      - 认证
    security:
      - Bearer: []
    responses:
      200:
        description: 获取成功
        schema:
          $ref: '#/definitions/ApiResponse'
      401:
        description: 未授权
        schema:
          $ref: '#/definitions/ApiResponse'
    """
    try:
        user_id = get_jwt_identity()
        user = UserService.get_by_id(user_id)
        if not user:
            return error_response(message='用户不存在', code=404)
        return success_response(data=user.to_dict(include_roles=True))
    except Exception as e:
        return error_response(message=str(e), code=500)


@bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """
    用户登出
    ---
    tags:
      - 认证
    security:
      - Bearer: []
    responses:
      200:
        description: 登出成功
        schema:
          $ref: '#/definitions/ApiResponse'
    """
    try:
        # JWT 是无状态的，客户端删除 token 即可
        # 这里可以添加 token 黑名单逻辑（需要 Redis）
        return success_response(message='登出成功')
    except Exception as e:
        return error_response(message=str(e), code=500)

