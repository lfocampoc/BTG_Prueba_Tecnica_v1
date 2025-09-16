from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

class SubscriptionStatus(str, Enum):
    ACTIVE = "active"
    CANCELLED = "cancelled"

class SubscriptionCreate(BaseModel):
    user_id: str
    fund_id: str
    amount: float = Field(..., gt=0)

class SubscriptionUpdate(BaseModel):
    status: Optional[SubscriptionStatus] = None
    amount: Optional[float] = Field(None, gt=0)

class Subscription(BaseModel):
    subscription_id: str
    user_id: str
    fund_id: str
    amount: float
    status: SubscriptionStatus
    created_at: str
    cancelled_at: Optional[str] = None

class SubscriptionResponse(BaseModel):
    subscription_id: str
    user_id: str
    fund_id: str
    amount: float
    status: str
    created_at: str
    cancelled_at: Optional[str] = None