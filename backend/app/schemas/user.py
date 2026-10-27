import uuid
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from app.models.enums import UserRole, UserStatus

class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    email: EmailStr
    full_name: str
    phone: str|None
    company: str|None
    role: UserRole
    status: UserStatus
    created_at: datetime
    last_login_at: datetime | None

class StaffCreate(BaseModel):
    full_name: str = Field(min_length=2, max_length=150)
    email: EmailStr
    phone: str|None = Field(default=None, max_length=30)
    temporary_password: str = Field(min_length=8, max_length=128)
    