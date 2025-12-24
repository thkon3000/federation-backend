from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.database import Base


class Club(Base):
    __tablename__ = "clubs"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    memberships = relationship(
        "Membership",
        back_populates="club",
        cascade="all, delete-orphan",
    )

    files = relationship(
        "File",
        back_populates="club",
        cascade="all, delete-orphan",
    )
