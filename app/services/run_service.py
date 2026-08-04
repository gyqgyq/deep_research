"""Run 业务逻辑。"""

import json
from typing import Any
from uuid import uuid4

from fastapi import HTTPException

from app.core.exceptions import NotFoundError
from app.enums import RunStatus
from app.models import AgentRuns
from app.repositories.run_repository import RunRepository
from app.utils.hash import string2hash
from app.api.deps import CurrentUser
from app.schemas.run_schema import (
    RunCreateRequest,
    RunCreateResponse,
    RunGetResponse,
    RunGetResponseInput,
    RunCancelRequest,
    RunCancelResponse,
)


def _json_to_optional_str(value: dict[str, Any] | None) -> str | None:
    """将 JSONB 字典转为响应中的可选字符串。"""
    if value is None:
        return None
    return json.dumps(value, ensure_ascii=False)


class RunService:
    """Run 创建"""

    def __init__(self, repository: RunRepository) -> None:
        self._repository = repository

    async def create_run(self, request: RunCreateRequest, user: CurrentUser) -> RunCreateResponse:
        """创建 run；同一 org 下相同幂等键返回已有记录。"""

        request_hash = string2hash(request.input.model_dump_json())
        existing = await self._repository.find_run_by_idempotency_key(
            user.org_id,
            request.idempotency_key,
        )
        if existing:
            # 幂等键相同，输入也相同，这是安全重试，则返回已有记录。
            if existing.request_hash == request_hash:
                return RunCreateResponse(
                    run_id=existing.id,
                    status=RunStatus(existing.status),
                    run_type=existing.run_type,
                    created_at=existing.created_at,
                )
            # 幂等键相同，输入不同，调用方用同一个键去做另一件事，必须拒绝
            raise HTTPException(
                status_code=409,
                detail={
                    "code": "CONFLICT",
                    "message": "该幂等键已被其他不同的请求入参占用使用",
                }
            )

        run = AgentRuns(
            id=str(uuid4()),
            org_id=user.org_id,
            user_id=user.user_id,
            run_type=request.run_type,
            status=RunStatus.QUEUED,
            idempotency_key=request.idempotency_key,
            request_hash=request_hash,
            input_json=request.input.model_dump(),
        )
        created = await self._repository.create(run)

        append_run_event(
            run_id=created.id,
            event_type='run.created',
            paylod={
                "status": created.status,
            }
        )

        return RunCreateResponse(
            run_id=created.id,
            status=RunStatus(created.status),
            run_type=created.run_type,
            created_at=created.created_at,
        )

    async def get_run(self, org_id: str, run_id: str) -> RunGetResponse:
        """按租户 + run_id 查询；不存在则 NotFoundError。"""
        run = await self._repository.get_run_by_id_and_org(run_id, org_id)

        if run is None:
            raise NotFoundError("run 不存在")

        input_data = run.input_json or {}
        return RunGetResponse(
            run_id=run.id,
            status=RunStatus(run.status),
            run_type=run.run_type,
            input=RunGetResponseInput(
                ticket_id=str(input_data.get("ticket_id", "")),
                order_id=str(input_data.get("order_id", "")),
            ),
            output=_json_to_optional_str(run.output_json),
            error=_json_to_optional_str(run.error_json),
            created_at=run.created_at,
            updated_at=run.updated_at,
            ended_at=run.ended_at,
        )

    async def cancel_run(self, request: RunCancelRequest, user: CurrentUser, run_id: str) -> dict:
        """取消 run"""
        run = await self._repository.get_run_by_id_and_org(run_id, user.org_id)

        if run is None or run.user_id != user.user_id:
            raise NotFoundError("run 不存在")

        if run.status in RunStatus.terminal_statuses():
            raise HTTPException(
                status_code=409,
                detail={
                    "code": "CONFLICT",
                    "message": "任务已结束，无法取消",
                }
            )

        # 这里只是请求取消，真正停止由worker在安全点配合完成
        # if run.status == RunStatus.RUNNING:
        #     # 运行中不能由API直接改状态，work可能正在调用退款这类副作用工具
        #     # API只写取消请求标记和事件，真正的running -> cancelled 由worker在安全点配合完成
        #     mark_run_cancel_requested(
        #         run_id=run_id,
        #         requested_by=user.user_id,
        #         reason=request.reason,
        #     )
        #     append_run_event(
        #         run_id=run_id,
        #         event_type='run.cancel_requested',
        #         paylod={
        #             "reason": request.reason,
        #         }
        #     )
        # else:
        #     # queued / waiting_for_user 还没有worker在执行，可以直接进入cancelled状态
        #     transition_run(
        #         run_id=run_id,
        #         to_status=RunStatus.CANCELLED,
        #         reason=request.reason,
        #         actor_type="user",
        #         actor_id=user.user_id,
        #     )

        return RunCancelResponse(
            run_id=run_id,
            status=RunStatus.CANCELLED,
        )
