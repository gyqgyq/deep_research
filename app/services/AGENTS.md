# app/services — 业务逻辑

## 职责

- 编排 repository、必要时触发 `agents`、使用 `core` 能力
- 文件命名 `*_service.py`；由 `api/deps.py` 注入

## 约定

- 失败时抛 `AppError` / `UnauthorizedError` / `ConflictError` / `NotFoundError`
- 不导入 `fastapi.HTTPException`
- 可依赖 schemas、enums、utils、models（构造实体）、repositories、core、agents

## 禁止

- 直接操作 Redis key 命名散落各处（auth 键用 `refresh_token_key`）
- 在 service 里设置 Cookie 或写 Response 头（留给 api）
