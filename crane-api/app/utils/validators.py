"""数据验证工具"""
from typing import Any, Dict, List, Optional


def validate_required_fields(data: Dict[str, Any], required_fields: List[str]) -> Optional[str]:
    """验证必填字段"""
    missing_fields = [field for field in required_fields if field not in data or data[field] is None]
    if missing_fields:
        return f"缺少必填字段: {', '.join(missing_fields)}"
    return None


def validate_data_source_config(data_source_type: str, config: Dict[str, Any]) -> Optional[str]:
    """验证数据源配置"""
    common_fields = ['name', 'host', 'port']
    missing = validate_required_fields(config, common_fields)
    if missing:
        return missing
    
    # 验证端口范围
    if 'port' in config:
        port = config['port']
        if not isinstance(port, int) or port < 1 or port > 65535:
            return "端口号必须在1-65535之间"
    
    # 根据不同类型验证特定字段
    if data_source_type in ['hive', 'doris', 'mysql']:
        if 'database' not in config:
            return "缺少必填字段: database"
    
    if data_source_type == 'presto':
        if 'catalog' not in config:
            return "缺少必填字段: catalog"
    
    return None

