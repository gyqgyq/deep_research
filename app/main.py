from fastapi import FastAPI

from app.routers.run_router import router as run_router

app = FastAPI(title="UV + FastAPI Demo")

app.include_router(run_router)


    