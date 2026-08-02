"""
app/schemas/user.py

Pydantic schemas used for request validation and response formatting.
These define exactly what data the API accepts and returns -
they are separate from the SQLAlchemy models (models/user.py) on purpose,
so we never accidentally expose fields like `password_hash` to the client.
"""

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, field_validator


class UserRegisterRequest(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=150)
    company_name: str = Field(..., min_length=2, max_length=150)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    confirm_password: str = Field(..., min_length=8, max_length=128)

    @field_validator("confirm_password")
    @classmethod
    def passwords_match(cls, confirm_password: str, info):
        password = info.data.get("password")
        if password and confirm_password != password:
            raise ValueError("Passwords do not match")
        return confirm_password


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=1)


class UserResponse(BaseModel):
    id: int
    full_name: str
    company_name: str
    email: EmailStr
    role: str
    created_at: datetime

    class Config:
        from_attributes = True  # allows creating this schema directly from an ORM object


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class MessageResponse(BaseModel):
    success: bool
    message: str
