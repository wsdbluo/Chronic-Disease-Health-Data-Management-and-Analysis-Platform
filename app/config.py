import os

from dotenv import load_dotenv

# 从项目根目录的 .env 文件加载环境变量
load_dotenv()


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY")

    # 启动时检查,避免漏配 .env 后出现难以理解的报错
    if not SQLALCHEMY_DATABASE_URI or not SECRET_KEY:
        raise RuntimeError(
            "缺少环境变量:请确认项目根目录存在 .env 文件,且已配置 DATABASE_URL 和 SECRET_KEY"
        )