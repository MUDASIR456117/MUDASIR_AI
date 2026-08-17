# REST API Specification — AI Financial Advisor

All endpoints are prefixed with `/api/v1` and generate interactive OpenAPI docs at `http://localhost:8000/docs`.

---

## 1. Authentication & Users
- `POST /api/v1/auth/register`: Create a new user account with hashed password and return access token.
- `POST /api/v1/auth/login`: Authenticate email/password credentials and issue signed JWT bearer token.
- `GET /api/v1/auth/me`: Retrieve current active user profile and permissions.
- `GET /api/v1/users/profile`: Retrieve user profile details.
- `PUT /api/v1/users/profile`: Update user parameters (monthly income, risk tolerance, display preferences).

## 2. Financial Dashboard & Analytics
- `GET /api/v1/dashboard/metrics`: Comprehensive dashboard aggregations (KPI cards, 6-month trends, category donut, dynamic AI insights).
- `GET /api/v1/income/`: Monthly and quarterly income inflows categorized by source.
- `GET /api/v1/expenses/analytics`: Granular expense breakdowns, Needs vs Wants 50/30 ratios, and Pareto distribution.

## 3. Transaction Management
- `POST /api/v1/transactions/`: Create transaction with automatic NLP categorization and real-time fraud anomaly scoring.
- `GET /api/v1/transactions/`: List and filter transactions (category, type, date range, pagination).
- `DELETE /api/v1/transactions/{id}`: Delete a transaction record.

## 4. Computer Vision & OCR Receipts
- `POST /api/v1/receipts/scan`: Upload multipart receipt image (JPG/PNG/PDF), run OpenCV image filtering and itemized text extraction.

## 5. AI Budgeting & Forecasting
- `GET /api/v1/budget/recommendation`: Dynamic 50/30/20 budget recommendation adjusted for user history.
- `GET /api/v1/budget/status`: Category limits, budget utilization percentages, and overspending warnings.
- `GET /api/v1/forecast/`: Time-series 30-day spending projection using Deep Learning LSTM and ensemble regressors.

## 6. Security, Fraud & Credit Risk
- `POST /api/v1/fraud/check`: Multi-feature anomaly scoring using Isolation Forest and Autoencoders.
- `GET /api/v1/fraud/alerts`: Logged historical anomaly events.
- `POST /api/v1/credit/evaluate`: Multi-factor credit risk model prediction with SHAP/Feature attribution and educational disclaimers.

## 7. Wealth & Portfolio Management
- `POST /api/v1/investments/risk-profile`: Classify investor profile (Conservative, Moderate, Aggressive) and target asset allocation.
- `GET /api/v1/portfolio/`: Holding positions, total invested, market value, unrealized gain/loss, and concentration risk.
- `GET /api/v1/goals/`: Active financial goals and monthly runway tracking.
- `POST /api/v1/goals/`: Create new financial goal.

## 8. Conversational AI Assistant & Reports
- `POST /api/v1/assistant/chat`: Context-aware chatbot processing natural language financial queries with user MongoDB context.
- `GET /api/v1/assistant/health-score`: Transparent 0-100 AI Financial Health Score with component breakdown.
- `POST /api/v1/reports/generate`: Generate official financial statements in PDF, CSV, or Excel formats.
- `GET /api/v1/reports/download/{filename}`: Download generated PDF document.

## 9. System Administration & Health
- `GET /health`: Health check endpoint (`status`, `database`, `models`).
- `GET /api/v1/admin/stats`: Enterprise stats, model registry, active users, and system audit logs.
