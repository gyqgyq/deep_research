from enum import StrEnum

class RunStatus(StrEnum):
    """任务状态"""
    QUEUED = "queued"
    RUNNING = "running"
    WAITING_FOR_USER_INPUT = "waiting_for_user_input"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELLED = "cancelled"