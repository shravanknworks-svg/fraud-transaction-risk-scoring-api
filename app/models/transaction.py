from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional


class TransactionChannel(str, Enum):
    WEB = "WEB"
    MOBILE = "MOBILE"
    ATM = "ATM"
    BRANCH = "BRANCH"
    API = "API"


class RiskDecision(str, Enum):
    APPROVE = "APPROVE"
    REVIEW = "REVIEW"
    DECLINE = "DECLINE"


class TransactionRequest(BaseModel):
    transaction_id: str = Field(..., examples=["TXN-1001"])
    customer_id: str = Field(..., examples=["CUST-501"])
    account_id: str = Field(..., examples=["ACC-9001"])
    amount: float = Field(..., gt=0, examples=[250.75])
    currency: str = Field(default="USD", examples=["USD"])
    merchant_category: str = Field(default="GENERAL", examples=["ELECTRONICS"])
    country: str = Field(default="US", examples=["US"])
    channel: TransactionChannel = TransactionChannel.WEB
    device_id: Optional[str] = Field(default=None, examples=["DEVICE-123"])
    ip_address: Optional[str] = Field(default=None, examples=["192.168.1.1"])
    transaction_time: datetime = Field(default_factory=datetime.utcnow)


class RiskResponse(BaseModel):
    transaction_id: str
    customer_id: str
    risk_score: int
    decision: RiskDecision
    reasons: list[str]
    evaluated_at: datetime
