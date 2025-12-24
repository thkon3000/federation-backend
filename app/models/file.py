from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.database import Base


class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True)

    club_id = Column(Integer, ForeignKey("clubs.id", ondelete="CASCADE"), nullable=False)
    uploaded_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))

    filename = Column(String(255), nullable=False)
    storage_path = Column(String(500), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    club = relationship("Club", back_populates="files")
    uploader = relationship("User")
