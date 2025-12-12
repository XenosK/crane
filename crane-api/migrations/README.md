# 数据库迁移

使用Flask-Migrate管理数据库迁移。

## 初始化迁移（首次使用）
```bash
flask db init
```

## 创建迁移
```bash
flask db migrate -m "描述信息"
```

## 应用迁移
```bash
flask db upgrade
```

## 回滚迁移
```bash
flask db downgrade
```

