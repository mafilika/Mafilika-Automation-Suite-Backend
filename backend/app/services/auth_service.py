"""
app/services/auth_service.py

Business logic for authentication. Route handlers stay thin and just
call into these functions - this keeps main.py / routes readable and
makes the logic reusable and testable.
"""

from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password
from app.models.user import User
from app.models.activity import UserActivity
from app.schemas.user import UserRegisterRequest


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email.lower()).first()


def create_user(db: Session, payload: UserRegisterRequest) -> User:
    """Create a new user with a securely hashed password."""
    new_user = User(
        full_name=payload.full_name.strip(),
        company_name=payload.company_name.strip(),
        email=payload.email.lower(),
        password_hash=hash_password(payload.password),
        role="owner",
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    log_activity(db, new_user.id, "register")
    return new_user


def authenticate_user(db: Session, email: str, password: str) -> User | None:
    """Return the user if the email/password combination is valid, else None."""
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user


def log_activity(db: Session, user_id: int, action: str) -> None:
    """Record an entry in the user_activity table."""
    activity = UserActivity(user_id=user_id, action=action)
    db.add(activity)
    db.commit()
