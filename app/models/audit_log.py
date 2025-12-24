from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime

from app.db.database import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    action = Column(String(100), nullable=False)
    resource_type = Column(String(100), nullable=False)
    resource_id = Column(Integer)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
