"""应用启动文件"""
from app import create_app
from app.config import config
import os

app = create_app(config.get(os.environ.get('FLASK_ENV', 'development')))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

