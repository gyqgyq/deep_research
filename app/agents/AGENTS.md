# app/agents — Agent 运行时

## 职责

- 执行编排：启动 / 取消 / 恢复 run
- 后续对接模型调用、工具调用、step/event/checkpoint 持久化

## 现状

- `AgentRuntime` 为空壳（`NotImplementedError`），尚未接入 LLM 或队列
- 由 **service** 触发，不直接挂 FastAPI 路由

## 约定

- 可依赖 `core`、`repositories`、`models`、`enums`
- 与 HTTP 解耦：不读 Request、不设 Cookie

## 禁止

- 在 agents 中写 REST 路由
- 未实现前在 api 层假装已跑通完整执行链路
