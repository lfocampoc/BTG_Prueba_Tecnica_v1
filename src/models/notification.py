from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

class NotificationType(str, Enum):
    SUBSCRIPTION_CONFIRMATION = "subscription_confirmation"
    CANCELLATION_CONFIRMATION = "cancellation_confirmation"

class NotificationChannel(str, Enum):
    EMAIL = "email"
    SMS = "sms"

class NotificationStatus(str, Enum):
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"

class NotificationCreate(BaseModel):
    user_id: str
    type: NotificationType
    channel: NotificationChannel
    content: str
    status: NotificationStatus = NotificationStatus.PENDING

class Notification(BaseModel):
    notification_id: str
    user_id: str
    type: NotificationType
    channel: NotificationChannel
    status: NotificationStatus
    content: str
    created_at: str
    sent_at: Optional[str] = None

class NotificationResponse(BaseModel):
    notification_id: str
    user_id: str
    type: str
    channel: str
    status: str
    content: str
    created_at: str
    sent_at: Optional[str] = None