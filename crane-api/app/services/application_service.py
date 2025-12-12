"""应用管理服务"""
from typing import List, Optional, Dict, Any
from app.models.application import Application
from app.extensions import db


class ApplicationService:
    """应用管理服务类"""
    
    @staticmethod
    def get_all(page: int = 1, page_size: int = 20, status: Optional[str] = None) -> Dict[str, Any]:
        """获取应用列表"""
        query = Application.query
        
        if status:
            query = query.filter(Application.status == status)
        
        pagination = query.order_by(Application.created_at.desc()).paginate(
            page=page, per_page=page_size, error_out=False
        )
        
        return {
            'items': [app.to_dict() for app in pagination.items],
            'total': pagination.total,
            'page': page,
            'page_size': page_size,
            'pages': pagination.pages
        }
    
    @staticmethod
    def get_by_id(app_id: int) -> Optional[Application]:
        """根据ID获取应用"""
        return Application.query.get(app_id)
    
    @staticmethod
    def create(data: Dict[str, Any]) -> Application:
        """创建应用"""
        application = Application(
            name=data['name'],
            description=data.get('description'),
            owner=data.get('owner'),
            status=data.get('status', 'active'),
            config=data.get('config')
        )
        db.session.add(application)
        db.session.commit()
        return application
    
    @staticmethod
    def update(app_id: int, data: Dict[str, Any]) -> Optional[Application]:
        """更新应用"""
        application = Application.query.get(app_id)
        if not application:
            return None
        
        if 'name' in data:
            application.name = data['name']
        if 'description' in data:
            application.description = data.get('description')
        if 'owner' in data:
            application.owner = data.get('owner')
        if 'status' in data:
            application.status = data['status']
        if 'config' in data:
            application.config = data['config']
        
        db.session.commit()
        return application
    
    @staticmethod
    def delete(app_id: int) -> bool:
        """删除应用"""
        application = Application.query.get(app_id)
        if not application:
            return False
        
        db.session.delete(application)
        db.session.commit()
        return True

