from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class TransactionType(str, Enum):
    INCOME = "INCOME"
    EXPENSE = "EXPENSE"
    TRANSFER = "TRANSFER"
    INVESTMENT = "INVESTMENT"

class TransactionCategory(str, Enum):
    FOOD = "Food"
    GROCERY = "Grocery"
    RENT = "Rent"
    UTILITIES = "Utilities"
    TRANSPORT = "Transport"
    FUEL = "Fuel"
    SHOPPING = "Shopping"
    ENTERTAINMENT = "Entertainment"
    EDUCATION = "Education"
    HEALTHCARE = "Healthcare"
    TRAVEL = "Travel"
    SALARY = "Salary"
    FREELANCING = "Freelancing"
    BUSINESS = "Business"
    INVESTMENT = "Investment"
    OTHER = "Other"

class TransactionBase(BaseModel):
    type: TransactionType = TransactionType.EXPENSE
    category: str = "Other"
    amount: float = Field(..., gt=0)
    currency: str = "USD"
    description: str
    merchant: Optional[str] = ""
    date: datetime = Field(default_factory=datetime.utcnow)
    payment_method: Optional[str] = "Credit Card"
    location: Optional[str] = "Online"
    status: Optional[str] = "COMPLETED"

class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(BaseModel):
    type: Optional[TransactionType] = None
    category: Optional[str] = None
    amount: Optional[float] = None
    description: Optional[str] = None
    merchant: Optional[str] = None
    date: Optional[datetime] = None
    payment_method: Optional[str] = None
    location: Optional[str] = None
    status: Optional[str] = None

class TransactionResponse(TransactionBase):
    id: str
    user_id: str
    created_at: datetime
    is_anomaly: Optional[bool] = False
    anomaly_score: Optional[float] = 0.0

class TransactionFilter(BaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    type: Optional[TransactionType] = None
    category: Optional[str] = None
    min_amount: Optional[float] = None
    max_amount: Optional[float] = None
    search: Optional[str] = None
    limit: int = 100
    skip: int = 0
