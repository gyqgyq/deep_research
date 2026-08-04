from enum import StrEnum


class RunStatus(StrEnum):
    """任务状态"""
    QUEUED = "queued"
    RUNNING = "running"
    WAITING_FOR_USER_INPUT = "waiting_for_user_input"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELLED = "cancelled"

    @classmethod
    def terminal_statuses(cls) -> list[str]:
        return [
            cls.SUCCEEDED,
            cls.FAILED,
            cls.CANCELLED,
        ]


class RunEventType(StrEnum):
    """Run 事件类型。"""
    CREATED = "run.created"
    CANCEL_REQUESTED = "run.cancel_requested"
    RESUMED = "run.resumed"