# federation_app/models.py
from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    DateTime,
    Text,
)
from sqlalchemy.orm import relationship

from .database import Base


class Club(Base):
    __tablename__ = "clubs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    code = Column(String(50), unique=True, nullable=True)  # optional short code
    city = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    members = relationship("Member", back_populates="club", cascade="all, delete-orphan")
    users = relationship("User", back_populates="club")
    files = relationship("ClubFile", back_populates="club")


class User(Base):
    """
    User accounts for login.

    - Federation admins: role="federation_admin", club_id = NULL
    - Club admins:      role="club_admin",       club_id = <club.id>
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(150), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False)  # "federation_admin" or "club_admin"
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    club_id = Column(Integer, ForeignKey("clubs.id"), nullable=True)
    club = relationship("Club", back_populates="users")


class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=True, index=True)
    phone = Column(String(50), nullable=True)
    national_id = Column(String(50), nullable=True, index=True)  # AMKA/AFM/etc if needed

    # Example fields for activity & history
    is_active = Column(Boolean, default=True)
    last_renewal_year = Column(Integer, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    club_id = Column(Integer, ForeignKey("clubs.id"), nullable=True)
    club = relationship("Club", back_populates="members")


class ClubFile(Base):
    __tablename__ = "club_files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    blob_path = Column(String(500), nullable=False)  # path/key in Azure Blob Storage
    tags = Column(String(255), nullable=True)

    uploaded_at = Column(DateTime, default=datetime.utcnow)
    uploaded_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    club_id = Column(Integer, ForeignKey("clubs.id"), nullable=False)
    club = relationship("Club", back_populates="files")
