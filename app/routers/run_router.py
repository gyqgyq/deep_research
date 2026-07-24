from fastapi import APIRouter


router = APIRouter()

@router.post("/runs")
async def runs_create():
    return {"msg": "Hello FastAPI with uv"}

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