"""统一响应格式"""
from flask import jsonify
from typing import Any, Optional


def success_response(data: Any = None, message: str = "操作成功", code: int = 200):
    """成功响应"""
    return jsonify({
        'code': code,
        'message': message,
        'data': data
    }), code


def error_response(message: str = "操作失败", code: int = 400, data: Any = None):
    """错误响应"""
    return jsonify({
        'code': code,
        'message': message,
        'data': data
    }), code


def paginated_response(data: list, total: int, page: int, page_size: int, message: str = "查询成功"):
    """分页响应"""
    return jsonify({
        'code': 200,
        'message': message,
        'data': {
            'items': data,
            'total': total,
            'page': page,
            'page_size': page_size,
            'pages': (total + page_size - 1) // page_size if page_size > 0 else 0
        }
    }), 200

