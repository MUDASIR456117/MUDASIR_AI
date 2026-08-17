import pytest
from datetime import datetime
from backend.app.schemas.transaction import TransactionCreate, TransactionType

def test_transaction_schema_validation():
    tx = TransactionCreate(
        description="Whole Foods organic milk and groceries",
        merchant="Whole Foods",
        amount=54.20,
        type=TransactionType.EXPENSE,
        category="Grocery"
    )
    assert tx.amount == 54.20
    assert tx.type == TransactionType.EXPENSE
    assert tx.category == "Grocery"
    assert tx.currency == "USD"

def test_negative_transaction_amount_rejected():
    with pytest.raises(Exception):
        TransactionCreate(
            description="Invalid test",
            amount=-20.0,
            type=TransactionType.EXPENSE
        )
