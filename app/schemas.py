from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


class MemberBase(BaseModel):
    first_name: str = Field(
        ...,
        example="Juan",
        description="Member's first name"
    )
    last_name: str = Field(
        ...,
        example="Dela Cruz",
        description="Member's last name"
    )
    email: EmailStr = Field(
        ...,
        example="juan@pycon.ph",
        description="Member's email address (must be unique)"
    )
    membership_type: str = Field(
        ...,
        example="professional",
        description="Type of membership: student, professional, or speaker"
    )
    is_active: bool = Field(
        default=True,
        example=True,
        description="Whether the membership is currently active"
    )


class MemberCreate(MemberBase):
    """Schema for creating a new member"""

    class Config:
        json_schema_extra = {
            "example": {
                "first_name": "Maria",
                "last_name": "Santos",
                "email": "maria@pycon.ph",
                "membership_type": "student",
                "is_active": True
            }
        }


class MemberUpdate(BaseModel):
    """Schema for updating an existing member (all fields optional)"""

    first_name: Optional[str] = Field(
        None,
        example="Juan",
        description="Updated first name"
    )
    last_name: Optional[str] = Field(
        None,
        example="Reyes",
        description="Updated last name"
    )
    email: Optional[EmailStr] = Field(
        None,
        example="juan.reyes@pycon.ph",
        description="Updated email address"
    )
    membership_type: Optional[str] = Field(
        None,
        example="speaker",
        description="Updated membership type"
    )
    is_active: Optional[bool] = Field(
        None,
        example=False,
        description="Updated active status"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "membership_type": "speaker",
                "is_active": True
            }
        }


class MemberResponse(MemberBase):
    """Schema for member response (includes auto-generated fields)"""

    id: int = Field(
        ...,
        example=1,
        description="Unique member ID (auto-generated)"
    )
    joined_date: datetime = Field(
        ...,
        example="2024-01-15T10:30:00",
        description="Timestamp when member joined"
    )
    updated_at: datetime = Field(
        ...,
        example="2024-01-15T10:30:00",
        description="Timestamp of last update"
    )

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "first_name": "Juan",
                "last_name": "Dela Cruz",
                "email": "juan@pycon.ph",
                "membership_type": "professional",
                "is_active": True,
                "joined_date": "2024-01-15T10:30:00",
                "updated_at": "2024-01-15T10:30:00"
            }
        }
