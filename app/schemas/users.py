from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    display_name: str = Field(min_length=1, max_length=255)


class UserUpdate(BaseModel):
    display_name: str | None = Field(default=None, min_length=1, max_length=255)
    active: bool | None = None


class UserRead(BaseModel):
    id: int
    email: EmailStr
    display_name: str
    created_at: datetime
    active: bool

    model_config = ConfigDict(from_attributes=True)
