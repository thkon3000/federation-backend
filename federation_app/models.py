# federation_app/models.py
from sqlalchemy import UniqueConstraint, Date
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, func, Text
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String(150), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)

    role = Column(String(50), nullable=False, default="club_admin")
    club_id = Column(Integer, ForeignKey("clubs.id"), nullable=True)

    is_active = Column(Boolean, nullable=False, server_default="true")
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    club = relationship("Club", back_populates="users")


class Club(Base):
    __tablename__ = "clubs"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(200), unique=True, index=True, nullable=False)
    code = Column(String(50), unique=True, index=True, nullable=False)
    city = Column(String(120), nullable=False)

    is_active = Column(Boolean, nullable=False, server_default="true")
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    users = relationship("User", back_populates="club")
    files = relationship("ClubFile", back_populates="club")


class ClubFile(Base):
    __tablename__ = "club_files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    blob_path = Column(String(500), nullable=False)
    tags = Column(String(255), nullable=True)
    notes = Column(Text, nullable=True)

    uploaded_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    uploaded_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    club_id = Column(Integer, ForeignKey("clubs.id"), nullable=False)
    club = relationship("Club", back_populates="files")

class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True)

    # --- Club relation ---
    club_id = Column(Integer, ForeignKey("clubs.id"), nullable=False)

    # --- Core member info ---
    registry_number = Column(String(50), nullable=False)  # ΑΡΙΘΜΟΣ ΜΗΤΡΩΟΥ
    last_name = Column(String(150), nullable=False)       # ΕΠΩΝΥΜΟ
    first_name = Column(String(150), nullable=False)      # ΟΝΟΜΑ
    father_name = Column(String(150), nullable=True)      # ΟΝΟΜΑ ΠΑΤΕΡΑ
    mother_name = Column(String(150), nullable=True)      # ΟΝΟΜΑ ΜΗΤΕΡΑΣ

    date_of_birth = Column(Date, nullable=True)           # ΗΜ/ΝΙΑ ΓΕΝΝΗΣΗΣ
    registration_date = Column(Date, nullable=True)       # ΗΜΕΡ ΕΓΓΡΑΦΗΣ
    last_renewal_date = Column(Date, nullable=True)       # ΤΕΛΕΥΤΑΙΑ ΑΝΑΝΕΩΣΗ

    # --- Identification ---
    id_number = Column(String(100), nullable=True)        # ΑΡ ΔΕΛΤΙΟΥ ΤΑΥΤΟΤΗΤΑΣ
    spouse_id_number = Column(String(100), nullable=True) # ΑΡ ΔΕΛΤΙΟΥ ΤΑΥΤΟΤΗΤΑΣ2

    # --- Financial / status ---
    receipt_number = Column(String(100), nullable=True)   # ΑΡΙΘΜΟΣ ΑΠΟΔΕΙΞΗΣ
    amount_paid = Column(String(50), nullable=True)       # ΠΟΣΟ
    year = Column(String(10), nullable=True)              # ΕΤΟΣ
    is_active = Column(Boolean, nullable=False, server_default="true")  # ΕΝΗΜΕΡΟΣ

    # --- Spouse ---
    spouse_last_name = Column(String(150), nullable=True)
    spouse_first_name = Column(String(150), nullable=True)
    spouse_father_name = Column(String(150), nullable=True)
    spouse_date_of_birth = Column(Date, nullable=True)

    # --- Children (fixed Excel structure) ---
    child1_last_name = Column(String(150), nullable=True)
    child1_first_name = Column(String(150), nullable=True)
    child1_date_of_birth = Column(Date, nullable=True)

    child2_last_name = Column(String(150), nullable=True)
    child2_first_name = Column(String(150), nullable=True)
    child2_date_of_birth = Column(Date, nullable=True)

    child3_last_name = Column(String(150), nullable=True)
    child3_first_name = Column(String(150), nullable=True)
    child3_date_of_birth = Column(Date, nullable=True)

    # --- Notes ---
    notes = Column(Text, nullable=True)

    # --- Soft delete / audit ---
    is_deleted = Column(Boolean, nullable=False, server_default="false")
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    __table_args__ = (
        UniqueConstraint("club_id", "registry_number", name="uq_member_registry_per_club"),
    )


