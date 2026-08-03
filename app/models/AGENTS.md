# app/models — ORM 模型

## 职责

- 表结构映射；文件命名 `*_model.py`
- 继承 `app.db.base.Base`

## 约定

- 仅描述持久化结构（列、FK、索引）
- 由 repository 访问；service / api 不直接拼查询（除极少数依赖注入取当前用户）

## 禁止

- 在 model 中写业务编排或 HTTP 相关代码
- 为「方便」把 Pydantic schema 逻辑塞进 ORM
