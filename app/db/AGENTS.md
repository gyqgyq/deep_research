# app/db — 数据基础设施

## 职责

- `base.py`：SQLAlchemy `DeclarativeBase`
- `session.py`：异步引擎、sessionmaker、`get_db`
- `redis.py`：Redis 客户端单例

## 约定

- 从具体子模块导入，避免经 `__init__.py` 聚合引发循环依赖
- 可依赖 `app.core.settings` 与 `app.core.db_url`
- 会话成功则 commit、异常则 rollback（见 `get_db`）

## 禁止

- 业务 Redis key 命名（如 `auth:refresh:*`）——放 `core.security`
- 在本层写业务逻辑、HTTP、领域校验
