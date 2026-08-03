# app/enums — 领域枚举

## 职责

- 跨层共享的状态/类型枚举（如 `RunStatus`）

## 约定

- 枚举值与数据库/API 字符串保持一致
- schemas 与 services 共用同一枚举，避免魔法字符串

## 禁止

- 在 enums 中依赖 db / FastAPI / repository
