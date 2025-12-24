from sqlalchemy import Column, Integer, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import relationship

from app.db.database import Base


class Membership(Base):
    __tablename__ = "memberships"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    club_id = Column(Integer, ForeignKey("clubs.id", ondelete="CASCADE"), nullable=False)

    club_role = Column(String(50), nullable=False)

    user = relationship("User", back_populates="memberships")
    club = relationship("Club", back_populates="memberships")

    __table_args__ = (
        UniqueConstraint("user_id", "club_id", name="uq_user_club"),
    )
