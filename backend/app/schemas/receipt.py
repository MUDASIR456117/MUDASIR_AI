from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class ReceiptItem(BaseModel):
    name: str
    quantity: float = 1.0
    price: float = 0.0

class ReceiptParseResult(BaseModel):
    merchant: Optional[str] = "Unknown Merchant"
    date: Optional[str] = None
    items: List[ReceiptItem] = Field(default_factory=list)
    subtotal: Optional[float] = 0.0
    tax: Optional[float] = 0.0
    total: float = 0.0
    payment_method: Optional[str] = "Credit Card"
    suggested_category: str = "Grocery"
    raw_text: Optional[str] = ""

class ReceiptResponse(BaseModel):
    id: str
    user_id: str
    filename: str
    file_path: str
    parsed_data: ReceiptParseResult
    transaction_id: Optional[str] = None
    created_at: datetime
