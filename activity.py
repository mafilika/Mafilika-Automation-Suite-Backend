"""
app/models/activity.py

Defines the `user_activity` table. Used to log important actions
(login, register, logout, and later: emails sent, reports generated, etc.)
so the dashboard and future audit/history features have real data to show.
"""

from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.database.database import Base


class UserActivity(Base):
    __tablename__ = "user_activity"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    action = Column(String(150), nullable=False)  # e.g. "login", "register", "logout"
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="activities")
