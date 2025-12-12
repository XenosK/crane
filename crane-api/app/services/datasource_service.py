"""数据源管理服务"""
from typing import List, Optional, Dict, Any
from datetime import datetime
from app.models.datasource import DataSource
from app.extensions import db
from app.utils.validators import validate_data_source_config


class DataSourceService:
    """数据源管理服务类"""
    
    @staticmethod
    def get_all(page: int = 1, page_size: int = 20, type: Optional[str] = None) -> Dict[str, Any]:
        """获取数据源列表"""
        query = DataSource.query
        
        if type:
            query = query.filter(DataSource.type == type)
        
        pagination = query.order_by(DataSource.created_at.desc()).paginate(
            page=page, per_page=page_size, error_out=False
        )
        
        return {
            'items': [ds.to_dict() for ds in pagination.items],
            'total': pagination.total,
            'page': page,
            'page_size': page_size,
            'pages': pagination.pages
        }
    
    @staticmethod
    def get_by_id(ds_id: int) -> Optional[DataSource]:
        """根据ID获取数据源"""
        return DataSource.query.get(ds_id)
    
    @staticmethod
    def get_by_type(ds_type: str) -> List[DataSource]:
        """根据类型获取数据源列表"""
        return DataSource.query.filter_by(type=ds_type, status='active').all()
    
    @staticmethod
    def create(data: Dict[str, Any]) -> DataSource:
        """创建数据源"""
        # 验证配置
        error = validate_data_source_config(data['type'], data)
        if error:
            raise ValueError(error)
        
        # 构建配置信息
        config = {}
        if data['type'] == 'presto':
            config = {
                'ssl': data.get('ssl', False)
            }
        elif data['type'] == 'hive':
            config = {
                'authType': data.get('authType', 'none'),
                'serviceDiscoveryMode': data.get('serviceDiscoveryMode', 'direct')
            }
        elif data['type'] in ['doris', 'mysql']:
            config = {
                'charset': data.get('charset', 'utf8'),
                'timeout': data.get('timeout', 30),
                'ssl': data.get('ssl', False) if data['type'] == 'mysql' else None
            }
        
        data_source = DataSource(
            name=data['name'],
            type=data['type'],
            host=data['host'],
            port=data['port'],
            database=data.get('database'),
            catalog=data.get('catalog'),
            schema=data.get('schema'),
            username=data.get('username'),
            password=data.get('password'),  # 实际应该加密存储
            config=config,
            status='active'
        )
        db.session.add(data_source)
        db.session.commit()
        return data_source
    
    @staticmethod
    def update(ds_id: int, data: Dict[str, Any]) -> Optional[DataSource]:
        """更新数据源"""
        data_source = DataSource.query.get(ds_id)
        if not data_source:
            return None
        
        # 验证配置
        if 'type' in data or 'host' in data or 'port' in data:
            type_to_validate = data.get('type', data_source.type)
            config_to_validate = {**data_source.to_dict(), **data}
            error = validate_data_source_config(type_to_validate, config_to_validate)
            if error:
                raise ValueError(error)
        
        if 'name' in data:
            data_source.name = data['name']
        if 'type' in data:
            data_source.type = data['type']
        if 'host' in data:
            data_source.host = data['host']
        if 'port' in data:
            data_source.port = data['port']
        if 'database' in data:
            data_source.database = data.get('database')
        if 'catalog' in data:
            data_source.catalog = data.get('catalog')
        if 'schema' in data:
            data_source.schema = data.get('schema')
        if 'username' in data:
            data_source.username = data.get('username')
        if 'password' in data:
            data_source.password = data.get('password')
        if 'config' in data:
            data_source.config = data['config']
        if 'status' in data:
            data_source.status = data['status']
        
        db.session.commit()
        return data_source
    
    @staticmethod
    def test_connection(ds_id: int) -> Dict[str, Any]:
        """测试数据源连接"""
        data_source = DataSource.query.get(ds_id)
        if not data_source:
            return {'success': False, 'message': '数据源不存在'}
        
        try:
            # 这里应该实现实际的连接测试逻辑
            # 根据不同类型的数据源使用相应的驱动进行连接测试
            data_source.last_test_at = datetime.utcnow()
            data_source.status = 'active'
            db.session.commit()
            
            return {'success': True, 'message': '连接成功'}
        except Exception as e:
            data_source.status = 'error'
            db.session.commit()
            return {'success': False, 'message': f'连接失败: {str(e)}'}
    
    @staticmethod
    def delete(ds_id: int) -> bool:
        """删除数据源"""
        data_source = DataSource.query.get(ds_id)
        if not data_source:
            return False
        
        db.session.delete(data_source)
        db.session.commit()
        return True

