"""系统管理服务"""
from typing import List, Optional, Dict, Any
from app.models.system import User, Role, Permission
from app.extensions import db


class UserService:
    """用户管理服务类"""
    
    @staticmethod
    def get_all(page: int = 1, page_size: int = 20, status: Optional[str] = None) -> Dict[str, Any]:
        """获取用户列表"""
        query = User.query
        
        if status:
            query = query.filter(User.status == status)
        
        pagination = query.order_by(User.created_at.desc()).paginate(
            page=page, per_page=page_size, error_out=False
        )
        
        return {
            'items': [user.to_dict(include_roles=True) for user in pagination.items],
            'total': pagination.total,
            'page': page,
            'page_size': page_size,
            'pages': pagination.pages
        }
    
    @staticmethod
    def get_by_id(user_id: int) -> Optional[User]:
        """根据ID获取用户"""
        return User.query.get(user_id)
    
    @staticmethod
    def get_by_username(username: str) -> Optional[User]:
        """根据用户名获取用户"""
        return User.query.filter_by(username=username).first()
    
    @staticmethod
    def create(data: Dict[str, Any]) -> User:
        """创建用户"""
        user = User(
            username=data['username'],
            email=data.get('email'),
            real_name=data.get('real_name'),
            phone=data.get('phone'),
            status=data.get('status', 'active')
        )
        user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()
        return user
    
    @staticmethod
    def update(user_id: int, data: Dict[str, Any]) -> Optional[User]:
        """更新用户"""
        user = User.query.get(user_id)
        if not user:
            return None
        
        if 'email' in data:
            user.email = data['email']
        if 'real_name' in data:
            user.real_name = data.get('real_name')
        if 'phone' in data:
            user.phone = data.get('phone')
        if 'status' in data:
            user.status = data['status']
        if 'password' in data:
            user.set_password(data['password'])
        
        db.session.commit()
        return user
    
    @staticmethod
    def assign_roles(user_id: int, role_ids: List[int]) -> Optional[User]:
        """分配角色"""
        user = User.query.get(user_id)
        if not user:
            return None
        
        roles = Role.query.filter(Role.id.in_(role_ids)).all()
        user.roles = roles
        db.session.commit()
        return user
    
    @staticmethod
    def delete(user_id: int) -> bool:
        """删除用户"""
        user = User.query.get(user_id)
        if not user:
            return False
        
        db.session.delete(user)
        db.session.commit()
        return True


class RoleService:
    """角色管理服务类"""
    
    @staticmethod
    def get_all(page: int = 1, page_size: int = 20, status: Optional[str] = None) -> Dict[str, Any]:
        """获取角色列表"""
        query = Role.query
        
        if status:
            query = query.filter(Role.status == status)
        
        pagination = query.order_by(Role.created_at.desc()).paginate(
            page=page, per_page=page_size, error_out=False
        )
        
        return {
            'items': [role.to_dict(include_permissions=True) for role in pagination.items],
            'total': pagination.total,
            'page': page,
            'page_size': page_size,
            'pages': pagination.pages
        }
    
    @staticmethod
    def get_by_id(role_id: int) -> Optional[Role]:
        """根据ID获取角色"""
        return Role.query.get(role_id)
    
    @staticmethod
    def create(data: Dict[str, Any]) -> Role:
        """创建角色"""
        role = Role(
            name=data['name'],
            code=data['code'],
            description=data.get('description'),
            status=data.get('status', 'active')
        )
        db.session.add(role)
        db.session.commit()
        return role
    
    @staticmethod
    def update(role_id: int, data: Dict[str, Any]) -> Optional[Role]:
        """更新角色"""
        role = Role.query.get(role_id)
        if not role:
            return None
        
        if 'name' in data:
            role.name = data['name']
        if 'code' in data:
            role.code = data['code']
        if 'description' in data:
            role.description = data.get('description')
        if 'status' in data:
            role.status = data['status']
        
        db.session.commit()
        return role
    
    @staticmethod
    def assign_permissions(role_id: int, permission_ids: List[int]) -> Optional[Role]:
        """分配权限"""
        role = Role.query.get(role_id)
        if not role:
            return None
        
        permissions = Permission.query.filter(Permission.id.in_(permission_ids)).all()
        role.permissions = permissions
        db.session.commit()
        return role
    
    @staticmethod
    def delete(role_id: int) -> bool:
        """删除角色"""
        role = Role.query.get(role_id)
        if not role:
            return False
        
        db.session.delete(role)
        db.session.commit()
        return True


class PermissionService:
    """权限管理服务类"""
    
    @staticmethod
    def get_all(page: int = 1, page_size: int = 20, resource: Optional[str] = None) -> Dict[str, Any]:
        """获取权限列表"""
        query = Permission.query
        
        if resource:
            query = query.filter(Permission.resource == resource)
        
        pagination = query.order_by(Permission.created_at.desc()).paginate(
            page=page, per_page=page_size, error_out=False
        )
        
        return {
            'items': [perm.to_dict(include_children=True) for perm in pagination.items],
            'total': pagination.total,
            'page': page,
            'page_size': page_size,
            'pages': pagination.pages
        }
    
    @staticmethod
    def get_by_id(permission_id: int) -> Optional[Permission]:
        """根据ID获取权限"""
        return Permission.query.get(permission_id)
    
    @staticmethod
    def create(data: Dict[str, Any]) -> Permission:
        """创建权限"""
        permission = Permission(
            name=data['name'],
            code=data['code'],
            resource=data.get('resource'),
            action=data.get('action'),
            path=data.get('path'),
            description=data.get('description'),
            parent_id=data.get('parent_id'),
            status=data.get('status', 'active')
        )
        db.session.add(permission)
        db.session.commit()
        return permission
    
    @staticmethod
    def update(permission_id: int, data: Dict[str, Any]) -> Optional[Permission]:
        """更新权限"""
        permission = Permission.query.get(permission_id)
        if not permission:
            return None
        
        if 'name' in data:
            permission.name = data['name']
        if 'code' in data:
            permission.code = data['code']
        if 'resource' in data:
            permission.resource = data.get('resource')
        if 'action' in data:
            permission.action = data.get('action')
        if 'path' in data:
            permission.path = data.get('path')
        if 'description' in data:
            permission.description = data.get('description')
        if 'parent_id' in data:
            permission.parent_id = data.get('parent_id')
        if 'status' in data:
            permission.status = data['status']
        
        db.session.commit()
        return permission
    
    @staticmethod
    def delete(permission_id: int) -> bool:
        """删除权限"""
        permission = Permission.query.get(permission_id)
        if not permission:
            return False
        
        db.session.delete(permission)
        db.session.commit()
        return True

