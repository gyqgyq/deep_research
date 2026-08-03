"""Run 业务逻辑。"""

import json
from typing import Any
from uuid import uuid4

from app.core.exceptions import NotFoundError
from app.enums import RunStatus
from app.models import AgentRuns
from app.repositories.run_repository import RunRepository
from app.schemas.run_schema import (
    RunCreateRequest,
    RunCreateResponse,
    RunGetRequest,
    RunGetRequestInput,
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

    async def create_run(self, request: RunCreateRequest) -> RunCreateResponse:
        """创建 run；同一 org 下相同幂等键返回已有记录。"""
        # existing = await self._repository.get_by_idempotency_key(
        #     request.org_id,
        #     request.idempotency_key,
        # )
        # if existing is not None:
        #     return RunCreateResponse(
        #         run_id=existing.id,
        #         status=RunStatus(existing.status),
        #         run_type=existing.run_type,
        #         created_at=existing.created_at,
        #     )

        run = AgentRuns(
            id=str(uuid4()),
            org_id=request.org_id,
            user_id=request.user_id,
            run_type=request.run_type,
            status=RunStatus.QUEUED,
            idempotency_key=request.idempotency_key,
            input_json=request.input.model_dump(),
        )
        created = await self._repository.create(run)
        return RunCreateResponse(
            run_id=created.id,
            status=RunStatus(created.status),
            run_type=created.run_type,
            created_at=created.created_at,
        )

    async def get_run(self, org_id: str, run_id: str) -> RunGetRequest:
        """按租户查询 run，不存在则 NotFoundError。"""
        run = await self._repository.get_by_id(org_id, run_id)
        if run is None:
            raise NotFoundError("run 不存在")

        input_data = run.input_json or {}
        return RunGetRequest(
            run_id=run.id,
            status=RunStatus(run.status),
            run_type=run.run_type,
            input=RunGetRequestInput(
                ticket_id=str(input_data.get("ticket_id", "")),
                order_id=str(input_data.get("order_id", "")),
            ),
            output=_json_to_optional_str(run.output_json),
            error=_json_to_optional_str(run.error_json),
            created_at=run.created_at,
            updated_at=run.updated_at,
            ended_at=run.ended_at,
        )
