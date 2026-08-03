# Deep Research Backend


## 目录结构

```text
app/
  api/                 # HTTP 层
    deps.py            # 依赖注入（如 get_db）
    v1/                # /api/v1 路由
  agents/              # Agent 运行时编排（当前为空壳）
  core/                # 配置、安全、日志、领域异常
  db/                  # 引擎、会话、ORM Base、Redis 客户端
  models/              # SQLAlchemy 模型
  schemas/             # Pydantic 请求/响应
  services/            # 业务逻辑
  repositories/        # 数据访问
  enums/               # 枚举
  utils/               # 工具
  main.py              # 应用入口（create_app）
alembic/               # 数据库迁移
```

## 环境配置

```bash
cp .env.example .env
```

编辑 `.env`

## 依赖与启动

```bash
uv sync
source .venv/Scripts/activate # git bash
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- 健康检查：`GET /api/v1/health`
- 就绪检查：`GET /api/v1/ready`
- OpenAPI：`http://127.0.0.1:8000/docs`

## 数据库迁移

```bash
uv run alembic revision --autogenerate -m "描述"
uv run alembic upgrade head
```
