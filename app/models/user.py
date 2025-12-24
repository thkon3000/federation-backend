from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base
from sqlalchemy.orm import relationship

memberships = relationship(
    "Membership",
    back_populates="user",
    cascade="all, delete-orphan",
)

audit_logs = relationship("AuditLog")


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    # admin | viewer
    global_role: Mapped[str] = mapped_column(String(50), nullable=False, default="viewer")
