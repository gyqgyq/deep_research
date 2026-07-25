from fastapi import APIRouter, HTTPException, status

from app.schemas.run_schema import RunCreateRequest

router = APIRouter(prefix="/runs", tags=["runs"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def runs_create(request: RunCreateRequest) -> dict:
    """创建 Run（业务未实现）。"""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="尚未实现")


@router.get("/{run_id}")
async def runs_get(run_id: str) -> dict:
    """查询 Run（业务未实现）。"""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="尚未实现")


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
