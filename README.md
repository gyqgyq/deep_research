### 环境配置

1. 复制环境变量模板并填入云 PostgreSQL 连接串：

```bash
cp .env.example .env
```

### 依赖

```bash
uv sync
```

### 启动

```bash
uv run uvicorn app.main:app --reload
```

