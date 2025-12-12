"""系统管理模型"""
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db


# 用户角色关联表
user_role = db.Table(
    'user_role',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True),
    db.Column('created_at', db.DateTime, default=datetime.utcnow)
)

# 角色权限关联表
role_permission = db.Table(
    'role_permission',
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True),
    db.Column('permission_id', db.Integer, db.ForeignKey('permissions.id'), primary_key=True),
    db.Column('created_at', db.DateTime, default=datetime.utcnow)
)


class User(db.Model):
    """用户模型"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True, comment='用户名')
    email = db.Column(db.String(100), unique=True, comment='邮箱')
    password_hash = db.Column(db.String(255), nullable=False, comment='密码哈希')
    real_name = db.Column(db.String(50), comment='真实姓名')
    phone = db.Column(db.String(20), comment='手机号')
    status = db.Column(db.String(20), default='active', comment='状态: active, inactive, locked')
    last_login = db.Column(db.DateTime, comment='最后登录时间')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')
    
    # 关联角色
    roles = db.relationship('Role', secondary=user_role, backref=db.backref('users', lazy='dynamic'), lazy='dynamic')
    
    def set_password(self, password):
        """设置密码"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """验证密码"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self, include_roles=False):
        """转换为字典"""
        data = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'real_name': self.real_name,
            'phone': self.phone,
            'status': self.status,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
        if include_roles:
            data['roles'] = [role.to_dict() for role in self.roles]
        return data
    
    def __repr__(self):
        return f'<User {self.username}>'


class Role(db.Model):
    """角色模型"""
    __tablename__ = 'roles'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True, comment='角色名称')
    code = db.Column(db.String(50), nullable=False, unique=True, comment='角色代码')
    description = db.Column(db.Text, comment='角色描述')
    status = db.Column(db.String(20), default='active', comment='状态: active, inactive')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')
    
    # 关联权限
    permissions = db.relationship('Permission', secondary=role_permission, backref=db.backref('roles', lazy='dynamic'), lazy='dynamic')
    
    def to_dict(self, include_permissions=False):
        """转换为字典"""
        data = {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'description': self.description,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
        if include_permissions:
            data['permissions'] = [perm.to_dict() for perm in self.permissions]
        return data
    
    def __repr__(self):
        return f'<Role {self.name}>'


class Permission(db.Model):
    """权限模型"""
    __tablename__ = 'permissions'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, comment='权限名称')
    code = db.Column(db.String(100), nullable=False, unique=True, comment='权限代码')
    resource = db.Column(db.String(50), comment='资源类型: menu, button, data')
    action = db.Column(db.String(50), comment='操作类型: read, write, delete, etc.')
    path = db.Column(db.String(200), comment='资源路径')
    description = db.Column(db.Text, comment='权限描述')
    parent_id = db.Column(db.Integer, db.ForeignKey('permissions.id'), comment='父权限ID')
    status = db.Column(db.String(20), default='active', comment='状态: active, inactive')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')
    
    # 自关联
    children = db.relationship('Permission', backref=db.backref('parent', remote_side=[id]), lazy='dynamic')
    
    def to_dict(self, include_children=False):
        """转换为字典"""
        data = {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'resource': self.resource,
            'action': self.action,
            'path': self.path,
            'description': self.description,
            'parent_id': self.parent_id,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
        if include_children:
            data['children'] = [child.to_dict() for child in self.children]
        return data
    
    def __repr__(self):
        return f'<Permission {self.name}>'

