from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime

class ReportGenerateRequest(BaseModel):
    report_type: str = "monthly"  # "monthly", "quarterly", "annual"
    period: str = "2026-08"  # e.g., "2026-08", "2026-Q3", "2026"
    format: str = "pdf"  # "pdf", "csv", "excel"

class ReportSummaryData(BaseModel):
    total_income: float
    total_expenses: float
    net_savings: float
    savings_rate_pct: float
    top_spending_category: str
    budget_adherence_pct: float
    anomaly_count: int
    health_score: int
    key_insights: List[str]

class ReportResponse(BaseModel):
    id: str
    report_type: str
    period: str
    file_format: str
    download_url: str
    summary: ReportSummaryData
    created_at: datetime
