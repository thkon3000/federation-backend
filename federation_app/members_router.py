# federation_app/members_router.py

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from .database import get_db
from .models import Member, User
from .schemas.member import MemberOut
from .auth_utils import get_current_user, enforce_club_scope
from .excel_utils import read_members_excel, parse_date

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
# IMPORT MEMBERS FROM EXCEL
# ----------------------------------
@router.post("/import")
def import_members(
    club_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    enforce_club_scope(club_id, current_user)

    if not file.filename.endswith(".xlsx"):
        raise HTTPException(status_code=400, detail="Only .xlsx files are supported")

    content = file.file.read()

    try:
        rows = read_members_excel(content)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    created = 0
    updated = 0
    errors = []

    for record in rows:
        row_num = record.get("_row")

        # Required fields
        registry_number = str(record.get("ΑΡΙΘΜΟΣ ΜΗΤΡΩΟΥ", "")).strip()
        last_name = record.get("ΕΠΩΝΥΜΟ")
        first_name = record.get("ΟΝΟΜΑ")

        # Skip empty / invalid rows silently
        if not registry_number or not last_name or not first_name:
            continue

        member = (
            db.query(Member)
            .filter(
                Member.club_id == club_id,
                Member.registry_number == registry_number,
            )
            .first()
        )

        data = {
            "club_id": club_id,
            "registry_number": registry_number,
            "last_name": last_name,
            "first_name": first_name,
            "father_name": record.get("ΟΝΟΜΑ ΠΑΤΕΡΑ"),
            "mother_name": record.get("ΟΝΟΜΑ ΜΗΤΕΡΑΣ"),
            "date_of_birth": parse_date(record.get("ΗΜ/ΝΙΑ ΓΕΝΝΗΣΗΣ")),
            "registration_date": parse_date(record.get("ΗΜΕΡ ΕΓΓΡΑΦΗΣ")),
            "last_renewal_date": parse_date(record.get("ΤΕΛΕΥΤΑΙΑ ΑΝΑΝΕΩΣΗ")),
            "id_number": record.get("ΑΡ ΔΕΛΤΙΟΥ ΤΑΥΤΟΤΗΤΑΣ"),
            "spouse_id_number": record.get("ΑΡ ΔΕΛΤΙΟΥ ΤΑΥΤΟΤΗΤΑΣ2"),
            "receipt_number": record.get("ΑΡΙΘΜΟΣ ΑΠΟΔΕΙΞΗΣ"),
            "amount_paid": record.get("ΠΟΣΟ"),
            "year": record.get("ΕΤΟΣ"),
            "is_active": str(record.get("ΕΝΗΜΕΡΟΣ", "")).strip() == "ΝΑΙ",
            "spouse_last_name": record.get("ΕΠΩΝΥΜΟ ΣΥΖΥΓΟΥ"),
            "spouse_first_name": record.get("ΟΝΟΜΑ ΣΥΖΥΓΟΥ"),
            "spouse_father_name": record.get("ΠΑΤΕΡΑΣ ΣΥΖΥΓΟΥ"),
            "spouse_date_of_birth": parse_date(record.get("ΗΜ ΓΕΝ ΣΥΖΥΓΟΥ")),
            "child1_last_name": record.get("ΕΠΩΝΥΜΟ ΤΕΚΝΟΥ 1"),
            "child1_first_name": record.get("ΟΝΟΜΑ ΤΕΚΝΟΥ 1"),
            "child1_date_of_birth": parse_date(record.get("ΗΜ ΓΕΝ ΤΕΚΝΟΥ 1")),
            "child2_last_name": record.get("ΕΠΩΝΥΜΟ ΤΕΚΝΟΥ 2"),
            "child2_first_name": record.get("ΟΝΟΜΑ ΤΕΚΝΟΥ 2"),
            "child2_date_of_birth": parse_date(record.get("ΗΜ ΓΕΝ ΤΕΚΝΟΥ 2")),
            "child3_last_name": record.get("ΕΠΩΝΥΜΟ ΤΕΚΝΟΥ 3"),
            "child3_first_name": record.get("ΟΝΟΜΑ ΤΕΚΝΟΥ 3"),
            "child3_date_of_birth": parse_date(record.get("ΗΜ ΓΕΝ ΤΕΚΝΟΥ 3")),
            "notes": record.get("ΠΑΡΑΤΗΡΗΣΕΙΣ"),
        }

        try:
            if member:
                for k, v in data.items():
                    setattr(member, k, v)
                updated += 1
            else:
                db.add(Member(**data))
                created += 1

            db.commit()
        except Exception as e:
            db.rollback()
            errors.append({"row": row_num, "reason": str(e)})

    return {
        "created": created,
        "updated": updated,
        "errors": errors,
    }
