# 数据库迁移

## 初始化数据库

使用项目根目录下的 `init_db.py` 脚本初始化数据库：

```bash
# 使用 uv（推荐）
uv run python init_db.py

# 或使用普通 Python
python init_db.py
```

该脚本会创建所有必需的数据表。

## 使用 Flask-Migrate（可选，用于生产环境）

如果需要使用 Flask-Migrate 进行数据库版本管理：

```bash
# 设置 Flask 应用
export FLASK_APP=run.py

# 初始化迁移（首次使用）
flask db init

# 创建迁移
flask db migrate -m "描述信息"

# 应用迁移
flask db upgrade

# 回滚迁移
flask db downgrade
```

