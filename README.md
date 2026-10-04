# 慢性病健康数据管理与分析平台

一个基于 **Flask + MySQL** 的慢性病健康数据管理与分析平台,用于记录和分析用户的血压、血糖、心率、体重等健康指标,通过可视化图表展示趋势,并基于医学参考值自动预警异常指标。

## ✨ 功能特性

- **用户认证**:注册、登录、退出,基于 Flask-Login 实现会话管理
- **密码安全**:密码使用 Werkzeug(scrypt)哈希加密存储,绝不存明文
- **健康数据管理**:血压、血糖、心率、体重的增删改查(CRUD)
- **服务端校验**:数值类型与合理范围校验,防止脏数据入库
- **数据隔离**:每个用户只能查看、编辑、删除自己的数据
- **统计分析**:平均值、最高/最低值等汇总指标
- **异常预警**:基于医学参考值自动识别异常指标(高血压、高血糖等)
- **数据可视化**:ECharts 折线图展示血压、血糖趋势

## 🛠 技术栈

| 类别 | 技术 |
|------|------|
| 后端框架 | Flask 3.x |
| ORM | Flask-SQLAlchemy + SQLAlchemy 2.x |
| 数据库驱动 | PyMySQL |
| 数据库 | MySQL 8.0 |
| 认证 | Flask-Login |
| 前端 | Jinja2 模板 + Bootstrap 5 + ECharts 5 |

## 📁 项目结构

```
manxingbing/
├── app/                      # 应用包
│   ├── __init__.py           # 应用工厂 create_app()
│   ├── config.py             # 配置(数据库连接等)
│   ├── extensions.py         # 扩展初始化(db、login_manager)
│   ├── models.py             # 数据模型(User、HealthRecord)
│   ├── blueprints/           # 路由蓝图
│   │   ├── main.py           # 首页
│   │   ├── auth.py           # 注册/登录/退出
│   │   └── records.py        # 健康数据 CRUD + 分析
│   └── templates/            # Jinja2 模板
│       └── records/          # 记录相关页面
├── run.py                    # 启动入口
└── requirements.txt          # 依赖清单
```

## 🚀 快速开始

### 环境要求

- Python 3.10+
- MySQL 8.0+

### 1. 创建数据库

```sql
CREATE DATABASE chronic_disease_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 2. 安装依赖

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows 激活虚拟环境
pip install -r requirements.txt
```

### 3. 配置数据库连接

编辑 `app/config.py`,把 `你的密码` 替换为你的 MySQL root 密码:

```python
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:你的密码@127.0.0.1:3306/chronic_disease_db?charset=utf8mb4"
```

### 4. 运行

```bash
python run.py
```

浏览器访问 http://127.0.0.1:5000 ,注册账号后即可使用。

## 📊 数据库设计

### users(用户表)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT | 主键,自增 |
| username | VARCHAR(64) | 用户名,唯一 |
| password_hash | VARCHAR(256) | 密码哈希 |
| role | VARCHAR(20) | 角色 |
| created_at | DATETIME | 注册时间 |

### health_records(健康记录表)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT | 主键,自增 |
| user_id | INT | 外键,关联 users.id |
| record_date | DATE | 记录日期 |
| systolic_bp | INT | 收缩压 |
| diastolic_bp | INT | 舒张压 |
| blood_glucose | FLOAT | 血糖 |
| heart_rate | INT | 心率 |
| weight | FLOAT | 体重 |
| note | VARCHAR(255) | 备注 |
| created_at | DATETIME | 录入时间 |

## 📝 后续可扩展

- 管理员后台(用户管理)
- 数据导出(Excel / PDF)
- 更多健康指标(BMI、体脂率)
- 单元测试
- Docker 部署
