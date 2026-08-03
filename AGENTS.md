# Deep Research Backend — Agent 指南

## 技术栈与入口

- FastAPI + SQLAlchemy(asyncio)/asyncpg + Alembic + Redis + JWT
- 包管理：`uv`；Python 3.11
- 启动：`uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`
- API 前缀：`settings.api_v1_prefix`（默认 `/api/v1`）

## 分层与依赖方向

```text
api → services → repositories → models → db.base
         ↘ schemas / enums / utils
         ↘ agents（运行时编排）
services / agents / db → core（settings / security / exceptions / db_url）
api → core / deps（HTTP 层可抛 HTTPException）
```

禁止反向依赖：`core` 不得依赖 `db` / `models` / `services`；`repositories` 不得依赖 FastAPI。

## 改码原则

1. 先读相关目录的 `AGENTS.md` 与现有实现，再增量修改
2. 对齐分层命名与挂载方式；能改一处不扩五处
3. Service 抛 `AppError` 族（见 `app/core/exceptions.py`），由 `main.py` 统一转 HTTP
4. Auth Redis key 等业务键放在 `core.security`，不进 `db`

## 模块索引

| 模块 | 文档 |
|------|------|
| HTTP | [app/api/AGENTS.md](app/api/AGENTS.md) |
| 配置与横切 | [app/core/AGENTS.md](app/core/AGENTS.md) |
| 基础设施 | [app/db/AGENTS.md](app/db/AGENTS.md) |
| ORM | [app/models/AGENTS.md](app/models/AGENTS.md) |
| DTO | [app/schemas/AGENTS.md](app/schemas/AGENTS.md) |
| 业务 | [app/services/AGENTS.md](app/services/AGENTS.md) |
| 数据访问 | [app/repositories/AGENTS.md](app/repositories/AGENTS.md) |
| 枚举 | [app/enums/AGENTS.md](app/enums/AGENTS.md) |
| 工具 | [app/utils/AGENTS.md](app/utils/AGENTS.md) |
| Agent 运行时 | [app/agents/AGENTS.md](app/agents/AGENTS.md) |

## 禁止

- 整层重写或无必要的大规模搬家
- Service 直接 `raise HTTPException`
- `core` 导入 `app.db.*`
- 在 `db` 层放业务 key 命名或领域逻辑
- 未确认用途就删除正在使用的模块
