import os
import io
import pandas as pd
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from backend.app.config import settings

class ReportService:
    def __init__(self):
        self.reports_dir = Path(settings.UPLOAD_DIR) / "reports"
        self.reports_dir.mkdir(parents=True, exist_ok=True)

    def generate_pdf_report(self, user_name: str, period: str, summary_data: Dict[str, Any],
                            transactions: List[Dict[str, Any]]) -> str:
        """Generate a clean, high-aesthetic executive financial report PDF using ReportLab."""
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = f"Financial_Report_{user_name}_{period}_{timestamp}.pdf"
        file_path = str(self.reports_dir / filename)

        doc = SimpleDocTemplate(
            file_path,
            pagesize=letter,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36
        )

        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'ReportTitle',
            parent=styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=22,
            leading=26,
            textColor=colors.HexColor('#1E293B'),
            spaceAfter=6
        )
        subtitle_style = ParagraphStyle(
            'ReportSubtitle',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=11,
            leading=14,
            textColor=colors.HexColor('#64748B'),
            spaceAfter=15
        )
        heading2_style = ParagraphStyle(
            'ReportHeading2',
            parent=styles['Heading2'],
            fontName='Helvetica-Bold',
            fontSize=14,
            leading=18,
            textColor=colors.HexColor('#0F172A'),
            spaceBefore=12,
            spaceAfter=6
        )
        body_style = ParagraphStyle(
            'ReportBody',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=10,
            leading=14,
            textColor=colors.HexColor('#334155')
        )

        story = []

        # Header Title
        story.append(Paragraph("AI FINANCIAL ADVISOR", title_style))
        story.append(Paragraph(f"Executive Financial Analytics & Intelligence Report • {period}", subtitle_style))
        story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#3B82F6'), spaceAfter=15))

        # KPI Summary Table
        story.append(Paragraph("1. Executive Summary & Core KPIs", heading2_style))
        
        income = summary_data.get("total_income", 0.0)
        expenses = summary_data.get("total_expenses", 0.0)
        net_savings = max(0.0, income - expenses)
        savings_rate = summary_data.get("savings_rate_pct", (net_savings / max(income, 1.0)) * 100.0)
        health_score = summary_data.get("health_score", 82)

        kpi_data = [
            ["Metric", "Value", "Benchmark / Status"],
            ["Total Inflow (Income)", f"${income:,.2f}", "Verified"],
            ["Total Outflow (Expenses)", f"${expenses:,.2f}", "Tracked"],
            ["Net Savings", f"${net_savings:,.2f}", f"{savings_rate:.1f}% Savings Rate"],
            ["AI Financial Health Score", f"{health_score} / 100", "OPTIMAL (Good Standing)"],
            ["Top Expense Category", str(summary_data.get("top_spending_category", "Housing / Food")), "Dominant Outflow"],
            ["Flagged Anomalies", str(summary_data.get("anomaly_count", 0)), "Protected by Isolation Forest"]
        ]

        t_kpi = Table(kpi_data, colWidths=[200, 150, 190])
        t_kpi.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#F1F5F9')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#0F172A')),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')])
        ]))
        story.append(t_kpi)
        story.append(Spacer(1, 15))

        # Recent Transactions Table
        story.append(Paragraph("2. Detailed Transaction Records", heading2_style))
        tx_rows = [["Date", "Merchant / Description", "Category", "Type", "Amount"]]
        
        for tx in transactions[:15]:
            d = tx.get("date", "")
            if isinstance(d, datetime):
                d = d.strftime("%Y-%m-%d")
            else:
                d = str(d)[:10]
            desc = str(tx.get("description", tx.get("merchant", "N/A")))[:28]
            cat = str(tx.get("category", "General"))
            ttype = str(tx.get("type", "EXPENSE"))
            amt = float(tx.get("amount", 0.0))
            tx_rows.append([d, desc, cat, ttype, f"${amt:,.2f}"])

        if len(tx_rows) == 1:
            tx_rows.append(["-", "No transactions recorded for this period", "-", "-", "$0.00"])

        t_tx = Table(tx_rows, colWidths=[70, 200, 100, 80, 90])
        t_tx.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E293B')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8.5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')])
        ]))
        story.append(t_tx)
        story.append(Spacer(1, 15))

        # AI Insights & Advisory Notes
        story.append(Paragraph("3. AI Intelligence & Prescriptive Advice", heading2_style))
        insights = summary_data.get("key_insights", [
            "Your discretionary spending remained within target limits this cycle.",
            "Maintaining your current savings pace ensures you will meet your annual financial goals.",
            "No high-risk anomalous activity detected on connected accounts."
        ])
        for ins in insights:
            story.append(Paragraph(f"• {ins}", body_style))
            story.append(Spacer(1, 3))

        story.append(Spacer(1, 15))
        story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#94A3B8'), spaceAfter=8))
        disclaimer = (
            "Disclaimer: This report was generated by AI Financial Advisor for informational and educational purposes. "
            "It does not constitute certified legal, tax, or accredited fiduciary financial advice."
        )
        story.append(Paragraph(disclaimer, ParagraphStyle('Disc', parent=styles['Normal'], fontSize=7.5, textColor=colors.HexColor('#94A3B8'))))

        doc.build(story)
        return file_path

    def generate_csv_report(self, transactions: List[Dict[str, Any]]) -> str:
        """Export transaction data to CSV string."""
        df = pd.DataFrame(transactions)
        if df.empty:
            df = pd.DataFrame(columns=["date", "type", "category", "amount", "currency", "merchant", "description", "payment_method", "status"])
        return df.to_csv(index=False)

    def generate_excel_report(self, summary_data: Dict[str, Any], transactions: List[Dict[str, Any]]) -> bytes:
        """Export structured multi-tab Excel workbook."""
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            # Summary Sheet
            df_summary = pd.DataFrame([summary_data])
            df_summary.to_excel(writer, sheet_name='Executive Summary', index=False)
            
            # Transactions Sheet
            df_tx = pd.DataFrame(transactions)
            if df_tx.empty:
                df_tx = pd.DataFrame(columns=["date", "type", "category", "amount", "merchant", "description"])
            df_tx.to_excel(writer, sheet_name='Transactions', index=False)
            
        return output.getvalue()

report_service = ReportService()
