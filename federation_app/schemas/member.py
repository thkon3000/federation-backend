# federation_app/schemas/member.py

from datetime import date, datetime
from pydantic import BaseModel
from typing import Optional


class MemberOut(BaseModel):
    id: int
    club_id: int

    registry_number: str
    last_name: str
    first_name: str
    father_name: Optional[str]
    mother_name: Optional[str]

    date_of_birth: Optional[date]
    registration_date: Optional[date]
    last_renewal_date: Optional[date]

    id_number: Optional[str]
    spouse_id_number: Optional[str]

    receipt_number: Optional[str]
    amount_paid: Optional[str]
    year: Optional[str]
    is_active: bool

    spouse_last_name: Optional[str]
    spouse_first_name: Optional[str]
    spouse_father_name: Optional[str]
    spouse_date_of_birth: Optional[date]

    child1_last_name: Optional[str]
    child1_first_name: Optional[str]
    child1_date_of_birth: Optional[date]

    child2_last_name: Optional[str]
    child2_first_name: Optional[str]
    child2_date_of_birth: Optional[date]

    child3_last_name: Optional[str]
    child3_first_name: Optional[str]
    child3_date_of_birth: Optional[date]

    notes: Optional[str]

    created_at: datetime

class Config:
    from_attributes = True

class MemberCreate(BaseModel):
    club_id: int
    registry_number: str

    last_name: str
    first_name: str
    father_name: Optional[str] = None
    mother_name: Optional[str] = None

    date_of_birth: Optional[date] = None
    registration_date: Optional[date] = None
    last_renewal_date: Optional[date] = None

    id_number: Optional[str] = None
    spouse_id_number: Optional[str] = None

    receipt_number: Optional[str] = None
    amount_paid: Optional[str] = None
    year: Optional[str] = None
    is_active: bool = True

    spouse_last_name: Optional[str] = None
    spouse_first_name: Optional[str] = None
    spouse_father_name: Optional[str] = None
    spouse_date_of_birth: Optional[date] = None

    child1_last_name: Optional[str] = None
    child1_first_name: Optional[str] = None
    child1_date_of_birth: Optional[date] = None

    child2_last_name: Optional[str] = None
    child2_first_name: Optional[str] = None
    child2_date_of_birth: Optional[date] = None

    child3_last_name: Optional[str] = None
    child3_first_name: Optional[str] = None
    child3_date_of_birth: Optional[date] = None

    notes: Optional[str] = None


class MemberUpdate(BaseModel):
    last_name: Optional[str] = None
    first_name: Optional[str] = None
    father_name: Optional[str] = None
    mother_name: Optional[str] = None

    date_of_birth: Optional[date] = None
    registration_date: Optional[date] = None
    last_renewal_date: Optional[date] = None

    id_number: Optional[str] = None
    spouse_id_number: Optional[str] = None

    receipt_number: Optional[str] = None
    amount_paid: Optional[str] = None
    year: Optional[str] = None
    is_active: Optional[bool] = None

    spouse_last_name: Optional[str] = None
    spouse_first_name: Optional[str] = None
    spouse_father_name: Optional[str] = None
    spouse_date_of_birth: Optional[date] = None

    child1_last_name: Optional[str] = None
    child1_first_name: Optional[str] = None
    child1_date_of_birth: Optional[date] = None

    child2_last_name: Optional[str] = None
    child2_first_name: Optional[str] = None
    child2_date_of_birth: Optional[date] = None

    child3_last_name: Optional[str] = None
    child3_first_name: Optional[str] = None
    child3_date_of_birth: Optional[date] = None

    notes: Optional[str] = None

