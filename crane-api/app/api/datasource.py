"""数据源管理API"""
from flask import Blueprint, request
from app.services.datasource_service import DataSourceService
from app.utils.response import success_response, error_response, paginated_response
from app.utils.validators import validate_required_fields

bp = Blueprint('datasource', __name__)


@bp.route('/list', methods=['GET'])
def get_datasource_list():
    """
    获取数据源列表
    ---
    tags:
      - 数据源管理
    parameters:
      - name: page
        in: query
        type: integer
        default: 1
        description: 页码
      - name: page_size
        in: query
        type: integer
        default: 20
        description: 每页数量
      - name: type
        in: query
        type: string
        enum: [presto, hive, doris, mysql]
        description: 数据源类型（可选）
    responses:
      200:
        description: 查询成功
        schema:
          $ref: '#/definitions/PaginatedResponse'
    """
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
    """
    获取数据源详情
    ---
    tags:
      - 数据源管理
    parameters:
      - name: ds_id
        in: path
        type: integer
        required: true
        description: 数据源ID
    responses:
      200:
        description: 查询成功
        schema:
          $ref: '#/definitions/ApiResponse'
      404:
        description: 数据源不存在
        schema:
          $ref: '#/definitions/ApiResponse'
    """
    try:
        data_source = DataSourceService.get_by_id(ds_id)
        if not data_source:
            return error_response(message='数据源不存在', code=404)
        return success_response(data=data_source.to_dict())
    except Exception as e:
        return error_response(message=str(e), code=500)


@bp.route('/type/<string:ds_type>', methods=['GET'])
def get_datasource_by_type(ds_type):
    """
    根据类型获取数据源列表
    ---
    tags:
      - 数据源管理
    parameters:
      - name: ds_type
        in: path
        type: string
        enum: [presto, hive, doris, mysql]
        required: true
        description: 数据源类型
    responses:
      200:
        description: 查询成功
        schema:
          $ref: '#/definitions/ApiResponse'
    """
    try:
        data_sources = DataSourceService.get_by_type(ds_type)
        return success_response(data=[ds.to_dict() for ds in data_sources])
    except Exception as e:
        return error_response(message=str(e), code=500)


@bp.route('/create', methods=['POST'])
def create_datasource():
    """
    创建数据源
    ---
    tags:
      - 数据源管理
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - name
            - type
            - host
            - port
          properties:
            name:
              type: string
              description: 数据源名称
              example: 生产环境Presto
            type:
              type: string
              enum: [presto, hive, doris, mysql]
              description: 数据源类型
              example: presto
            host:
              type: string
              description: 主机地址
              example: localhost
            port:
              type: integer
              description: 端口
              example: 8080
            database:
              type: string
              description: 数据库名称
            catalog:
              type: string
              description: Catalog (Presto)
            schema:
              type: string
              description: Schema
            username:
              type: string
              description: 用户名
            password:
              type: string
              description: 密码
            config:
              type: object
              description: 其他配置信息
    responses:
      200:
        description: 创建成功
        schema:
          $ref: '#/definitions/ApiResponse'
      400:
        description: 参数错误
        schema:
          $ref: '#/definitions/ApiResponse'
    """
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
    """
    更新数据源
    ---
    tags:
      - 数据源管理
    parameters:
      - name: ds_id
        in: path
        type: integer
        required: true
        description: 数据源ID
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              description: 数据源名称
            host:
              type: string
              description: 主机地址
            port:
              type: integer
              description: 端口
            database:
              type: string
              description: 数据库名称
            catalog:
              type: string
              description: Catalog
            schema:
              type: string
              description: Schema
            username:
              type: string
              description: 用户名
            password:
              type: string
              description: 密码
            config:
              type: object
              description: 配置信息
            status:
              type: string
              enum: [active, inactive, error]
              description: 状态
    responses:
      200:
        description: 更新成功
        schema:
          $ref: '#/definitions/ApiResponse'
      404:
        description: 数据源不存在
        schema:
          $ref: '#/definitions/ApiResponse'
      400:
        description: 参数错误
        schema:
          $ref: '#/definitions/ApiResponse'
    """
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
    """
    测试数据源连接
    ---
    tags:
      - 数据源管理
    parameters:
      - name: ds_id
        in: path
        type: integer
        required: true
        description: 数据源ID
    responses:
      200:
        description: 连接测试成功
        schema:
          $ref: '#/definitions/ApiResponse'
      400:
        description: 连接测试失败
        schema:
          $ref: '#/definitions/ApiResponse'
    """
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
    """
    删除数据源
    ---
    tags:
      - 数据源管理
    parameters:
      - name: ds_id
        in: path
        type: integer
        required: true
        description: 数据源ID
    responses:
      200:
        description: 删除成功
        schema:
          $ref: '#/definitions/ApiResponse'
      404:
        description: 数据源不存在
        schema:
          $ref: '#/definitions/ApiResponse'
    """
    try:
        success = DataSourceService.delete(ds_id)
        if not success:
            return error_response(message='数据源不存在', code=404)
        return success_response(message='删除成功')
    except Exception as e:
        return error_response(message=str(e), code=500)

