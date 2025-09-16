from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

class TransactionType(str, Enum):
    SUBSCRIPTION = "subscription"
    CANCELLATION = "cancellation"

class TransactionStatus(str, Enum):
    COMPLETED = "completed"
    FAILED = "failed"
    PENDING = "pending"

class TransactionCreate(BaseModel):
    user_id: str
    type: TransactionType
    fund_id: str
    amount: float = Field(..., gt=0)
    balance_before: float
    balance_after: float
    status: TransactionStatus = TransactionStatus.COMPLETED

class Transaction(BaseModel):
    transaction_id: str
    user_id: str
    type: TransactionType
    fund_id: str
    amount: float
    balance_before: float
    balance_after: float
    status: TransactionStatus
    created_at: str

class TransactionResponse(BaseModel):
    transaction_id: str
    user_id: str
    type: str
    fund_id: str
    amount: float
    balance_before: float
    balance_after: float
    status: str
    created_at: str