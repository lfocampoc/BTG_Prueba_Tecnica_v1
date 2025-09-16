from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

class FundCategory(str, Enum):
    FPV = "FPV"
    FIC = "FIC"
    DEUDAPRIVADA = "DEUDAPRIVADA"

class FundCreate(BaseModel):
    fund_id: str
    name: str
    category: FundCategory
    minimum_amount: float
    is_active: bool = True

class FundUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[FundCategory] = None
    minimum_amount: Optional[float] = None
    is_active: Optional[bool] = None

class Fund(BaseModel):
    fund_id: str
    name: str
    category: FundCategory
    minimum_amount: float
    is_active: bool
    created_at: str

class FundResponse(BaseModel):
    fund_id: str
    name: str
    category: str
    minimum_amount: float
    is_active: bool
    created_at: str