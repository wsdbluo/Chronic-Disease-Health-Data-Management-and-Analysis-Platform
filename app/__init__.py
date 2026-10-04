from flask import Flask

from app.config import Config
from app.extensions import db, login_manager


def create_app():
    app = Flask(__name__)      #创建 Flask 实例
    app.config.from_object(Config)      #加载配置 (Config)
    db.init_app(app)            #绑定数据库 (db)
    login_manager.init_app(app)     #绑定登录管理器 (login_manager)

    # 未登录时自动跳转到的页面
    login_manager.login_view = "auth.login"
    login_manager.login_message = "请先登录"

    from app import models  # noqa: F401    导入模型 → 建表 (create_all)

    with app.app_context():
        db.create_all()

    #注册蓝图 (main / auth / records)
    from app.blueprints.main import main_bp
    from app.blueprints.auth import auth_bp
    from app.blueprints.records import records_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(records_bp)

    return app      #返回成品 app