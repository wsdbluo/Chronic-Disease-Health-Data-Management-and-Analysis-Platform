from flask import Blueprint, render_template
from flask_login import login_required
from sqlalchemy import text

from app.extensions import db

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
@login_required
def index():
    return render_template("index.html")


@main_bp.route("/db-test")
def db_test():
    result = db.session.execute(text("SELECT 1"))
    return f"<h1>数据库连接成功</h1><p>查询结果: {result.scalar()}</p>"