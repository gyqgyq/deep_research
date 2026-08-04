from fastapi import APIRouter, Depends, HTTPException, Path, status

from app.api.deps import CurrentUser, get_run_service
from app.schemas.run_schema import RunCreateRequest, RunCreateResponse, RunGetResponse
from app.services.run_service import RunService

router = APIRouter(prefix="/runs", tags=["runs"])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=RunCreateResponse)
async def runs_create(
    user: CurrentUser,
    request: RunCreateRequest,
    service: RunService = Depends(get_run_service),
) -> RunCreateResponse:
    """创建 Run（支持幂等键去重）。"""
    return await service.create_run(request, user)


@router.get("/{run_id}", response_model=RunGetResponse)
async def runs_get(
    user: CurrentUser,
    run_id: str = Path(..., description="任务ID"),
    service: RunService = Depends(get_run_service),
) -> RunGetResponse:
    """查询 Run。"""
    return await service.get_run(user.org_id, run_id)


@router.get("/{run_id}/events")
async def runs_events(run_id: str) -> dict:
    """订阅 Run 事件（业务未实现）。"""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="尚未实现")


@router.post("/{run_id}/cancel")
async def runs_cancel(run_id: str) -> dict:
    """取消 Run（业务未实现）。"""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="尚未实现")


@router.post("/{run_id}/resume")
async def runs_resume(run_id: str) -> dict:
    """恢复 Run（业务未实现）。"""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="尚未实现")


@router.get("/{run_id}/trace")
async def runs_trace(run_id: str) -> dict:
    """查询 Run 轨迹（业务未实现）。"""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="尚未实现")
