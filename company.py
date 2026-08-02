"""
app/models/company.py

Defines the `companies` table. Each user (owner) can have one or more
company records, which future modules (CRM, reports, etc.) will attach to.
"""

from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.database.database import Base


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(150), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    industry = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    owner = relationship("User", back_populates="companies")
