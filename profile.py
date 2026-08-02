"""
app/routes/profile.py

Endpoint for the logged-in user's own profile:
- GET /api/profile
"""

from fastapi import APIRouter, Depends

from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.user import UserResponse

router = APIRouter(prefix="/api", tags=["Profile"])


@router.get("/profile", response_model=UserResponse)
def get_profile(current_user: User = Depends(get_current_user)):
    """Return the currently authenticated user's profile information."""
    return UserResponse.model_validate(current_user)
