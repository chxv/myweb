from flask import Flask
from .db import db
from flask_login import LoginManager

# 初始化数据库
db = db
login_manager = LoginManager()
login_manager.login_view = 'auth.login'  # 绑定


def create_app():
    from .config import Config
    from .route import register_all_route

    app = Flask(__name__)  # 初始化整体的app
    app.config.from_object(Config)  # 从类对象初始化自定义配置
    register_all_route(app)  # 调用包中的函数直接注册所有路由蓝本

    db.init_app(app)
    login_manager.init_app(app)

    return app


app = create_app()




