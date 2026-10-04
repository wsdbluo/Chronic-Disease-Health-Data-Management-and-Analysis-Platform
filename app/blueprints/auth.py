from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required

from app.extensions import db, login_manager
from app.models import User

auth_bp = Blueprint("auth", __name__)    #创建蓝图


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))   #按主键查用户,int(user_id) 把字符串 id 转成整数


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        #开始查询 users 表加上"用户名等于输入值"的条件取第一条结果,没有则返回 None
        if User.query.filter_by(username=username).first():
            #flash 提示 + redirect 跳回注册页
            flash("用户名已存在,请换一个")
            return redirect(url_for("auth.register"))

        user = User(username=username, role="patient")
        user.set_password(password)
        db.session.add(user)    #只是暂存
        db.session.commit()     #真正写库
        flash("注册成功!请登录")
        return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()
        if user is None or not user.check_password(password):
            flash("用户名或密码错误")
            return redirect(url_for("auth.login"))

        login_user(user)
        flash("登录成功!")
        return redirect(url_for("main.index"))

    return render_template("login.html")


@auth_bp.route("/logout")
@login_required     #这个页面必须登录才能访问
def logout():
    logout_user()   #清除会话
    flash("已退出登录")
    return redirect(url_for("main.index"))