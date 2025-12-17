# federation_app/club_router.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .database import get_db
from .models import Club, User
from .schemas import ClubCreate, ClubOut
from .auth_utils import get_current_user, enforce_club_scope

router = APIRouter(prefix="/api/clubs", tags=["clubs"])


# -------------------------
# CREATE CLUB
# -------------------------
@router.post("/", response_model=ClubOut, status_code=status.HTTP_201_CREATED)
def create_club(
    club_in: ClubCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "federation_admin":
        raise HTTPException(status_code=403, detail="Only federation admins can create clubs")

    club = Club(
        name=club_in.name,
        code=club_in.code,
        city=club_in.city,
    )
    db.add(club)
    db.commit()
    db.refresh(club)
    return club


# -------------------------
# LIST CLUBS (FEDERATION ONLY)
# -------------------------
@router.get("/", response_model=list[ClubOut])
def list_clubs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "federation_admin":
        raise HTTPException(status_code=403, detail="Only federation admins can list all clubs")

    return db.query(Club).order_by(Club.name).all()


# -------------------------
# GET CLUB BY ID
# -------------------------
@router.get("/{club_id}", response_model=ClubOut)
def get_club(
    club_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    club = db.query(Club).filter(Club.id == club_id).first()
    if not club:
        raise HTTPException(status_code=404, detail="Club not found")

    enforce_club_scope(club_id, current_user)
    return club


# -------------------------
# UPDATE CLUB (FEDERATION ONLY)
# -------------------------
@router.put("/{club_id}", response_model=ClubOut)
def update_club(
    club_id: int,
    club_in: ClubCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "federation_admin":
        raise HTTPException(status_code=403, detail="Only federation admins can update clubs")

    club = db.query(Club).filter(Club.id == club_id).first()
    if not club:
        raise HTTPException(status_code=404, detail="Club not found")

    club.name = club_in.name
    club.code = club_in.code
    club.city = club_in.city

    db.commit()
    db.refresh(club)
    return club
