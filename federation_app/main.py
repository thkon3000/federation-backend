# federation_app/main.py
from fastapi import FastAPI

from .database import Base, engine
from .auth_router import router as auth_router
# από εδώ και πέρα θα προσθέτουμε και τα άλλα routers (members, clubs, κλπ)


# Create tables on startup (για αρχική φάση, μετά μπορούμε να πάμε σε Alembic)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Federation Backend")


@app.get("/")
def root():
    return {"status": "ok"}


app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
