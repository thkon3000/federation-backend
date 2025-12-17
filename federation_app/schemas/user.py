from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from federation_app.database import get_db
from federation_app.models import User, Club
from federation_app.schemas.user import ClubAdminCreate, UserOut
from federation_app.auth_utils import (
    require_federation_admin,
    get_password_hash,
)

router = APIRouter(prefix="/api/users", tags=["users"])


@router.post(
    "/club-admin",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
)
def create_club_admin(
    data: ClubAdminCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_federation_admin),
):
    # ✅ check club exists
    club = db.get(Club, data.club_id)
    if not club:
        raise HTTPException(status_code=404, detail="Club not found")

    # ✅ unique username
    existing = db.query(User).filter(User.username == data.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")

    user = User(
        username=data.username,
        password_hash=get_password_hash(data.password),
        role="club_admin",
        club_id=data.club_id,
        is_active=True,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user
from pydantic import BaseModel


class ClubAdminCreate(BaseModel):
    username: str
    password: str
    club_id: int


class UserOut(BaseModel):
    id: int
    username: str
    role: str
    club_id: int | None

    class Config:
        from_attributes = True