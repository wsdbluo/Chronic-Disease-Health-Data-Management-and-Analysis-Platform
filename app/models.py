from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db


class User(db.Model, UserMixin):
    __tablename__ = "users"

    #db.Column(...)	定义一个列(字段)
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="patient")
    created_at = db.Column(db.DateTime, default=datetime.now)

    #声明User 和 HealthRecord 之间存在一对多关系
    records = db.relationship("HealthRecord", backref="user", lazy="dynamic")

    #把明文密码加密后存进 password_hash 字段(注册时用
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    #把用户输入的明文和库里的哈希比对,返回 True/False(登录时用)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"


class HealthRecord(db.Model):
    __tablename__ = "health_records"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    record_date = db.Column(db.Date, nullable=False)
    systolic_bp = db.Column(db.Integer)   # 收缩压(高压)
    diastolic_bp = db.Column(db.Integer)  # 舒张压(低压)
    blood_glucose = db.Column(db.Float)   # 血糖
    heart_rate = db.Column(db.Integer)    # 心率
    weight = db.Column(db.Float)          # 体重(kg)
    note = db.Column(db.String(255))      # 备注
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f"<HealthRecord {self.id} of user {self.user_id}>"