# federation_app/schemas/club.py

from pydantic import BaseModel
from datetime import datetime


class ClubCreate(BaseModel):
    name: str
    code: str
    city: str


class ClubOut(BaseModel):
    id: int
    name: str
    code: str
    city: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
