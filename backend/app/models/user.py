"""
app/models/user.py

Defines the `users` table. Each registered user has one row here.
Passwords are NEVER stored in plain text - only `password_hash` is saved.
"""

from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from app.database.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(150), nullable=False)
    company_name = Column(String(150), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), default="owner", nullable=False)  # e.g. owner, admin, staff
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # One user can own multiple companies and have multiple activity logs
    companies = relationship("Company", back_populates="owner", cascade="all, delete-orphan")
    activities = relationship("UserActivity", back_populates="user", cascade="all, delete-orphan")
