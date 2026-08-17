# 💎 AI FINANCIAL ADVISOR — ULTIMATE LEVEL
> **"Track. Predict. Protect. Grow."** — Intelligent AI-Powered Personal Financial Analytics & Prediction Platform

---

## 🌟 Executive Project Overview

**AI Financial Advisor** is an advanced, production-grade AI and Data Science platform built as a university final-year capstone and fintech portfolio centerpiece. Moving beyond basic CRUD trackers, it unifies **Natural Language Processing (NLP)**, **Computer Vision (CV)**, **Unsupervised Machine Learning**, **Recurrent Deep Learning (LSTM)**, and **Explainable AI (XAI)** to deliver real-time wealth intelligence and proactive risk protection.

---

## 🚀 Key Platform Capabilities

- 🤖 **NLP Expense Categorizer**: TF-IDF & Ensemble ML classifying transactions into 16 categories with confidence scores.
- 📷 **Computer Vision Receipt Scanner**: OpenCV bilateral filtering, adaptive Otsu thresholding, and OCR entity parsing for itemized receipts.
- 🛡️ **Isolation Forest Anomaly Guard**: Unsupervised outlier detection identifying spending spikes, timing anomalies (e.g. 3 AM charges), and novel merchants.
- 🧠 **Deep Autoencoder Anomaly Scoring**: Multi-layer neural network evaluating reconstruction error to surface hidden fraudulent patterns.
- 📈 **Deep Learning Time-Series Forecaster**: Recurrent LSTM network projecting 30-day forward cashflow trajectories with 90% confidence ribbon bands.
- 🎯 **Credit Risk Model & Explainable AI (XAI)**: Gradient-boosted default risk predictor equipped with transparent SHAP feature importance charts.
- 💎 **Intelligent Investment Advisor**: Risk profiler classifying investor archetypes (Conservative, Moderate, Aggressive) and managing portfolio concentration risk.
- 💬 **Conversational AI Financial Assistant**: Context-aware chatbot querying user MongoDB financial metrics to answer natural language queries.
- 🩺 **0–100 AI Financial Health Score**: Transparent index evaluating savings rate, expense-to-income, emergency runway, DTI, and budget discipline.
- 📑 **Audit-Ready Report Generator**: One-click generation of professional executive statements in **PDF**, **Excel (.xlsx)**, and **CSV** formats.
- ⚡ **Role-Based Admin Dashboard**: Enterprise metrics, model performance leaderboards, cluster telemetry, and audit logs.

---

## 🛠️ Technology Stack

| Layer | Technologies |
| :--- | :--- |
| **Backend** | Python 3.12, FastAPI, Uvicorn, Pydantic v2, Pydantic Settings |
| **Database** | MongoDB (`ai_financial_advisor`), Motor (Async), PyMongo (Sync & Aggregations) |
| **Frontend** | Streamlit (Ultimate Fintech UI), Custom CSS, Plotly Interactive Charts |
| **Machine Learning** | Scikit-Learn (TF-IDF, Logistic Regression, Random Forest, Isolation Forest, Gradient Boosting), Joblib |
| **Deep Learning** | TensorFlow 2.17+, Keras (LSTM Recurrent Networks, Deep Dense Autoencoders) |
| **Computer Vision** | OpenCV (cv2), Pillow, OCR text & regex entity extraction |
| **Explainable AI** | SHAP feature attribution weights & feature importance |
| **Reporting & Export** | ReportLab (PDF Engine), OpenPyXL, Pandas |
| **Security** | Bcrypt password hashing, PyJWT (JSON Web Tokens), RBAC (`USER` / `ADMIN`) |
| **Testing** | Pytest, Pytest-Asyncio, HTTPX TestClient |
| **DevOps** | Docker, Docker Compose |

---

## 📁 Project Directory Structure

```
AI-FINANCIAL-ADVISOR/
├── backend/
│   ├── app/
│   │   ├── main.py                     # FastAPI entry point, CORS, exception handlers, health check
│   │   ├── config.py                   # Pydantic-settings configuration
│   │   ├── database.py                 # Async/Sync MongoDB connection & index initializers
│   │   ├── api/v1/                     # 17 Domain-specific API routers
│   │   ├── schemas/                    # Pydantic v2 request/response models
│   │   ├── services/                   # Business logic services (ML, OCR, Reports, Assistant)
│   │   ├── repositories/               # MongoDB aggregation pipeline queries
│   │   └── security/                   # Bcrypt hashing, JWT tokens, RBAC dependencies
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/
│   ├── app.py                          # Streamlit main entry point with modern navigation
│   ├── pages/                          # 18 Modular Streamlit pages
│   ├── components/                     # Reusable UI cards, Plotly charts, AI insight boxes
│   ├── services/                       # API Client communicating with FastAPI backend
│   ├── styles/custom.css               # Luxury Fintech Dark CSS design system
│   └── Dockerfile
│
├── ml/
│   ├── datasets/                       # Synthetic financial datasets
│   ├── notebooks/                      # 10 Data Science Jupyter Notebooks (01 to 10)
│   ├── training/train_all_models.py    # Standalone model training pipeline
│   └── models/                         # Serialized model artifacts (.joblib, .keras)
│
├── tests/
│   ├── test_auth.py                    # Password hashing & JWT unit tests
│   ├── test_transactions.py            # Transaction schema unit tests
│   ├── test_ml.py                      # ML/DL inference & health score unit tests
│   └── test_api.py                     # FastAPI endpoint integration tests
│
├── docs/                               # Architecture, API, Database, Models & User Manual
├── generate_dataset.py                 # Synthetic dataset generator script
├── seed_database.py                    # Database seeding script for demo personas
├── docker-compose.yml                  # Full-stack multi-container deployment
├── .env.example                        # Template environment variables
└── README.md                           # Master Project Documentation
```

---

## ⚡ Quick Start & Setup Guide

### 1. Clone & Environment Setup
```bash
# Clone the repository
git clone <repository_url>
cd "FINAL PROJECT OF AI & DATASCEINCE "

# Create and activate virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Generate Datasets & Train Models
```bash
# Generate safe synthetic financial transactions & credit profiles
python generate_dataset.py

# Train all ML & Deep Learning models (saves artifacts to models/)
python ml/training/train_all_models.py

# Generate all 10 Data Science Jupyter Notebooks
python ml/notebooks/generate_notebooks.py
```

### 3. Seed MongoDB Database
```bash
# Ensure MongoDB is running on mongodb://localhost:27017
python seed_database.py
```

### 4. Start Backend & Frontend Servers

**Terminal 1 (FastAPI Backend):**
```bash
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```
- API Documentation: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/health`

**Terminal 2 (Streamlit Frontend):**
```bash
streamlit run frontend/app.py
```
- Web Application: `http://localhost:8501`

---

## 🔑 Demo Login Personas

| Persona | Email | Password | Role |
| :--- | :--- | :--- | :--- |
| **Demo User** (Alex Mercer) | `demo@financialadvisor.ai` | `Demo@12345` | `USER` |
| **Administrator** | `admin@financialadvisor.ai` | `Admin@12345` | `ADMIN` |

---

## 🐳 Docker Deployment

Run the complete platform (FastAPI + Streamlit + MongoDB) with a single command:
```bash
docker-compose up --build
```

---

## 🧪 Running Automated Tests

Execute the comprehensive test suite with Pytest:
```bash
pytest tests/ -v
```

---

## 📜 Educational & Compliance Disclaimer

*This application provides educational, analytical, and model-based estimates. It does not provide personalized regulated financial advice, nor does it guarantee investment returns or loan approvals.*
