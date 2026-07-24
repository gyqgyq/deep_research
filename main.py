from fastapi import FastAPI

app = FastAPI(title="UV + FastAPI Demo")

@app.get("/")
async def root():
    return {"msg": "Hello FastAPI with uv"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )