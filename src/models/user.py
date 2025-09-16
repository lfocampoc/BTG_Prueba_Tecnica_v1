from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    CLIENT = "client"
    ADMIN = "admin"

class NotificationPreference(str, Enum):
    EMAIL = "email"
    SMS = "sms"

class UserCreate(BaseModel):
    email: EmailStr
    phone: str = Field(..., min_length=10, max_length=15)
    password: str = Field(..., min_length=6)
    notification_preference: NotificationPreference = NotificationPreference.EMAIL
    # role se asigna automáticamente como CLIENT en el servicio

class UserUpdate(BaseModel):
    phone: Optional[str] = Field(None, min_length=10, max_length=15)
    notification_preference: Optional[NotificationPreference] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)

class User(BaseModel):
    user_id: str
    email: str
    phone: str
    balance: float = 500000.0  # Monto inicial
    notification_preference: NotificationPreference
    role: UserRole = UserRole.CLIENT
    created_at: str
    updated_at: str

class UserResponse(BaseModel):
    user_id: str
    email: str
    phone: str
    balance: float
    notification_preference: str
    role: str
    created_at: str
    updated_at: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse