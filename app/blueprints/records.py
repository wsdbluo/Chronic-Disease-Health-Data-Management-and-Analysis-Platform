from datetime import datetime

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from app.extensions import db
from app.models import HealthRecord

records_bp = Blueprint("records", __name__)


#把表单传来的"字符串"转成"数字",空值转成 None
def to_float(value):
    return float(value) if value else None


def to_int(value):
    return int(value) if value else None


def parse_record_form(form):
    """解析并校验表单。返回 (数据字典, 错误信息);错误信息为 None 表示校验通过。"""
    try:
        record_date = datetime.strptime(
            form.get("record_date"), "%Y-%m-%d"
        ).date()
    except (ValueError, TypeError):
        return None, "请选择有效的日期"

    try:
        systolic = to_int(form.get("systolic_bp"))
        diastolic = to_int(form.get("diastolic_bp"))
        glucose = to_float(form.get("blood_glucose"))
        heart = to_int(form.get("heart_rate"))
        weight = to_float(form.get("weight"))
    except ValueError:
        return None, "数值格式不正确,请检查"

    ranges = [
        (systolic, "收缩压", 0, 300),
        (diastolic, "舒张压", 0, 200),
        (glucose, "血糖", 0, 50),
        (heart, "心率", 0, 300),
        (weight, "体重", 0, 500),
    ]
    for value, name, low, high in ranges:
        if value is not None and not (low < value < high):
            return None, f"{name}数值不合理,应在 {low}~{high} 之间"

    values = {
        "record_date": record_date,
        "systolic_bp": systolic,
        "diastolic_bp": diastolic,
        "blood_glucose": glucose,
        "heart_rate": heart,
        "weight": weight,
        "note": form.get("note"),
    }
    return values, None

def average(values):
    """计算平均值,自动跳过空值"""
    vals = [v for v in values if v is not None]
    return round(sum(vals) / len(vals), 1) if vals else None


def check_alerts(record):
    """检查一条记录是否有异常指标,返回异常描述列表"""
    alerts = []
    if record.systolic_bp is not None:
        if record.systolic_bp >= 140:
            alerts.append("收缩压偏高")
        elif record.systolic_bp < 90:
            alerts.append("收缩压偏低")
    if record.diastolic_bp is not None:
        if record.diastolic_bp >= 90:
            alerts.append("舒张压偏高")
        elif record.diastolic_bp < 60:
            alerts.append("舒张压偏低")
    if record.blood_glucose is not None:
        if record.blood_glucose > 6.1:
            alerts.append("血糖偏高")
        elif record.blood_glucose < 3.9:
            alerts.append("血糖偏低")
    return alerts

@records_bp.route("/records")
@login_required         # ② 要求登录
def list_records():
    records = (
        HealthRecord.query      #开始查 health_records 表
        .filter_by(user_id=current_user.id)     #只查当前用户的记录(数据隔离)
        .order_by(HealthRecord.record_date.desc())      #按日期降序(新的在前)
        .all()      #取出所有结果,返回列表
    )

    # render_template("records/list.html", ...):渲染这个 HTML 模板;
    # records=records:把刚才查到的列表,以变量名 records 传给模板;
    return render_template("records/list.html", records=records)


@records_bp.route("/records/add", methods=["GET", "POST"])
@login_required
def add_record():
    if request.method == "POST":
        values, error = parse_record_form(request.form)
        if error:
            flash(error)
            return redirect(url_for("records.add_record"))

        record = HealthRecord(user_id=current_user.id, **values)
        db.session.add(record)
        db.session.commit()
        flash("记录添加成功!")
        return redirect(url_for("records.list_records"))

    return render_template("records/add.html")


@records_bp.route("/records/<int:record_id>/edit", methods=["GET", "POST"])
@login_required
def edit_record(record_id):
    record = HealthRecord.query.filter_by(
        id=record_id, user_id=current_user.id
    ).first_or_404()

    if request.method == "POST":
        values, error = parse_record_form(request.form)
        if error:
            flash(error)
            return redirect(url_for("records.edit_record", record_id=record_id))

        record.record_date = values["record_date"]
        record.systolic_bp = values["systolic_bp"]
        record.diastolic_bp = values["diastolic_bp"]
        record.blood_glucose = values["blood_glucose"]
        record.heart_rate = values["heart_rate"]
        record.weight = values["weight"]
        record.note = values["note"]
        db.session.commit()
        flash("记录已更新!")
        return redirect(url_for("records.list_records"))

    return render_template("records/edit.html", record=record)


@records_bp.route("/records/<int:record_id>/delete", methods=["POST"])
@login_required
def delete_record(record_id):
    record = HealthRecord.query.filter_by(
        id=record_id, user_id=current_user.id
    ).first_or_404()

    db.session.delete(record)
    db.session.commit()
    flash("记录已删除!")
    return redirect(url_for("records.list_records"))


@records_bp.route("/analysis")
@login_required
def analysis():
    records = (
        HealthRecord.query
        .filter_by(user_id=current_user.id)
        .order_by(HealthRecord.record_date.asc())
        .all()
    )

    dates = [r.record_date.strftime("%Y-%m-%d") for r in records]
    systolic = [r.systolic_bp for r in records]
    diastolic = [r.diastolic_bp for r in records]
    glucose = [r.blood_glucose for r in records]

    # 统计摘要
    systolic_valid = [v for v in systolic if v is not None]
    stats = {
        "count": len(records),
        "avg_systolic": average(systolic),
        "avg_diastolic": average(diastolic),
        "avg_glucose": average(glucose),
        "max_systolic": max(systolic_valid) if systolic_valid else None,
        "min_systolic": min(systolic_valid) if systolic_valid else None,
    }

    # 异常预警:逐条检查
    alerts = []
    for r in records:
        issues = check_alerts(r)
        if issues:
            alerts.append({"record": r, "issues": issues})

    return render_template(
        "records/analysis.html",
        dates=dates,
        systolic=systolic,
        diastolic=diastolic,
        glucose=glucose,
        stats=stats,
        alerts=alerts,
    )