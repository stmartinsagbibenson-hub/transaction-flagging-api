from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, Field


class TransactionRequest(BaseModel):
    transaction_id: str
    account_id: str
    amount: Decimal = Field(gt=0)
    currency: str = Field(min_length=3, max_length=3)
    transaction_type: Literal["withdrawal", "deposit", "transfer"]
    timestamp: datetime


class BatchRequest(BaseModel):
    transactions: list[dict] = Field(min_length=1, max_length=100)


class Flag(BaseModel):
    rule: str
    reason: str


class TransactionEvaluation(BaseModel):
    transaction_id: str
    account_id: str
    amount: Decimal
    currency: str
    risk_level: Literal["LOW", "MEDIUM", "HIGH"]
    flagged: bool
    flags: list[Flag]
    evaluated_at: datetime


class BatchItemResult(BaseModel):
    index: int
    success: bool
    result: TransactionEvaluation | None = None
    error: str | None = None


class BatchResponse(BaseModel):
    total: int
    successful: int
    failed: int
    results: list[BatchItemResult]