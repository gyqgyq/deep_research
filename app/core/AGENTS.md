# app/core — 配置与横切能力

## 职责

- `settings.py`：环境配置（pydantic-settings）
- `security.py`：JWT 签发/校验、auth Redis key
- `exceptions.py`：领域异常（`AppError` 及子类）
- `db_url.py`：数据库 URL 规范化（供 settings / session 使用）
- `logging.py`：日志初始化

## 约定

- 本层只依赖标准库与第三方库，以及本包内其它 core 模块
- URL 工具放在 `db_url.py`，不要放回 `app.db`

## 禁止

- `from app.db ...` / `from app.models ...` / `from app.services ...`
- 在 core 中写 FastAPI 路由或 ORM 查询
