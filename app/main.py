from fastapi import FastAPI

app = FastAPI(title="Federation Backend API")


@app.get("/health")
def health():
    return {"status": "ok"}
