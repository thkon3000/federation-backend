from fastapi import FastAPI

from app.routers.auth_router import router as auth_router

app = FastAPI(title="Federation Backend API")

app.include_router(auth_router)


@app.get("/health")
def health():
    return {"status": "ok"}
