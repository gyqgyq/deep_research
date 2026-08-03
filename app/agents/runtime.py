"""Agent 运行时编排占位。

后续接入点（由 service 触发，不直接依赖 FastAPI）：
- 启动 / 取消 / 恢复一次 agent run
- 读写 run、step、event、checkpoint、model_call、tool_call
- 调用外部模型与工具，写回用量与审计
"""


class AgentRuntime:
    """Agent 执行编排入口（空壳）。"""

    async def start(self, run_id: str) -> None:
        """启动指定 run 的执行。"""
        raise NotImplementedError("AgentRuntime.start 尚未实现")

    async def cancel(self, run_id: str) -> None:
        """取消正在执行的 run。"""
        raise NotImplementedError("AgentRuntime.cancel 尚未实现")

    async def resume(self, run_id: str) -> None:
        """从 checkpoint 恢复 run。"""
        raise NotImplementedError("AgentRuntime.resume 尚未实现")
