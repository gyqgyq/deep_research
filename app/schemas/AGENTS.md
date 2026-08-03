# app/schemas — Pydantic DTO

## 职责

- 请求/响应模型；与 ORM 分离
- 文件命名 `*_schema.py`

## 约定

- 可依赖 `app.enums`
- 字段校验与序列化放在 schema；业务规则放 service

## 禁止

- schema 依赖 repository / db session / FastAPI `Request`
- 用 ORM 模型直接当 API 响应模型（除非明确且已有先例）
