from fastapi import APIRouter

from app.schemas.run_schema import RunCreateRequest, RunCreateResponse

router = APIRouter()

@router.post("/runs", response_model=RunCreateResponse, status_code=201)
async def runs_create(
    request: RunCreateRequest,
):
    return {}

@router.get("/runs/{run_id}")
async def runs_get(run_id: str):
    return {"msg": "Hello FastAPI with uv"}

@router.get("/runs/{run_id}/events")
async def runs_events(run_id: str):
    return {"msg": "Hello FastAPI with uv"}

@router.post("/run/{run_id}/cancel")
async def runs_cancel(run_id: str):
    return {"msg": "Hello FastAPI with uv"}

@router.post("/run/{run_id}/resume")
async def runs_resume(run_id: str):
    return {"msg": "Hello FastAPI with uv"}

@router.get("/runs/{run_id}/trace")
async def runs_trace(run_id: str):
    return {"msg": "Hello FastAPI with uv"}