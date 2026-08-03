# app/repositories — 数据访问

## 职责

- 封装针对某一聚合/表的查询与持久化
- 文件命名 `*_repository.py`；构造函数接收 `AsyncSession`

## 约定

- 只依赖 `models` 与 SQLAlchemy
- 返回 ORM 实体或简单标量；不做 DTO 组装（除非已有明确先例）

## 禁止

- 导入 FastAPI / 抛 `HTTPException` / `AppError`
- 在 repository 里写跨聚合的业务规则（应上移 service）
