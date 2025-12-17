# federation_app/members_router.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from .database import get_db
from .models import Member, User
from .schemas.member import MemberOut, MemberCreate, MemberUpdate
from .auth_utils import get_current_user, enforce_club_scope

router = APIRouter(prefix="/api/members", tags=["members"])


# ----------------------------------
# GET ALL MEMBERS (FEDERATION / CLUB)
# ----------------------------------
@router.get("/", response_model=list[MemberOut])
def list_members(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Member).filter(Member.is_deleted == False)

    if current_user.role != "federation_admin":
        query = query.filter(Member.club_id == current_user.club_id)

    return query.order_by(Member.last_name, Member.first_name).all()


# ----------------------------------
# GET MEMBERS BY CLUB
# ----------------------------------
@router.get("/club/{club_id}", response_model=list[MemberOut])
def list_members_by_club(
    club_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    enforce_club_scope(club_id, current_user)

    return (
        db.query(Member)
        .filter(
            Member.club_id == club_id,
            Member.is_deleted == False,
        )
        .order_by(Member.last_name, Member.first_name)
        .all()
    )


# ----------------------------------
# CREATE MEMBER
# ----------------------------------
@router.post("/", response_model=MemberOut, status_code=status.HTTP_201_CREATED)
def create_member(
    member_in: MemberCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # club isolation
    enforce_club_scope(member_in.club_id, current_user)

    member = Member(**member_in.dict())

    db.add(member)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Registry number already exists for this club",
        )

    db.refresh(member)
    return member


# ----------------------------------
# UPDATE MEMBER
# ----------------------------------
@router.put("/{member_id}", response_model=MemberOut)
def update_member(
    member_id: int,
    member_in: MemberUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    member = (
        db.query(Member)
        .filter(Member.id == member_id, Member.is_deleted == False)
        .first()
    )
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    enforce_club_scope(member.club_id, current_user)

    for field, value in member_in.dict(exclude_unset=True).items():
        setattr(member, field, value)

    db.commit()
    db.refresh(member)
    return member


# ----------------------------------
# SOFT DELETE MEMBER
# ----------------------------------
@router.delete("/{member_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_member(
    member_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    member = (
        db.query(Member)
        .filter(Member.id == member_id, Member.is_deleted == False)
        .first()
    )
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    enforce_club_scope(member.club_id, current_user)

    member.is_deleted = True
    db.commit()
