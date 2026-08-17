# System Architecture — AI Financial Advisor

## High-Level Architectural Flow

```mermaid
graph TD
    User["End User / Browser"] -->|HTTP / REST (JWT)| StreamlitUI["Streamlit Frontend (18 Modular Pages)"]
    StreamlitUI -->|REST API v1| FastAPIGateway["FastAPI Gateway (Uvicorn)"]
    
    subgraph Security_Layer ["Security & Middleware"]
        CORS["CORS Middleware"]
        JWT_Auth["JWT Token Verification & RBAC"]
        RateLimit["Rate Limiting & Input Validation"]
    end
    
    FastAPIGateway --> Security_Layer
    
    subgraph Service_Layer ["Domain Service Layer"]
        AuthSvc["Auth & User Service"]
        TxSvc["Transaction & Budget Service"]
        ReportSvc["Report Generation Service (PDF/XLSX)"]
        ChatSvc["Conversational AI Context Engine"]
        InvestSvc["Investment & Portfolio Service"]
    end
    
    Security_Layer --> Service_Layer
    
    subgraph AI_Engine ["AI / ML / DL / Computer Vision"]
        ExpML["Expense Categorizer (TF-IDF + Ensemble)"]
        FraudML["Fraud Anomaly (Isolation Forest + Autoencoder)"]
        ForeDL["Spending Forecaster (LSTM / Recurrent Net)"]
        CreditML["Credit Risk Assessment + SHAP XAI"]
        CV_OCR["OpenCV Preprocessing + Receipt OCR"]
    end
    
    Service_Layer --> AI_Engine
    
    subgraph Data_Storage ["Persistence & Artifacts"]
        Mongo[("MongoDB Database (ai_financial_advisor)")]
        ModelsDisk["Serialized Models Directory (/models)"]
        UploadsDisk["Encrypted Uploads & Generated Reports"]
    end
    
    Service_Layer --> Mongo
    AI_Engine --> ModelsDisk
    ReportSvc --> UploadsDisk
```

---

## Architectural Principles

1. **Decoupled Client-Server Tier**: Streamlit UI consumes FastAPI endpoints via strict Pydantic v2 validation contracts.
2. **Stateless Scalable Backend**: Authentication is fully stateless using RS256/HS256 JWT bearer tokens with role-based authorization (`USER`, `ADMIN`).
3. **Dual Persistence & Aggregation**: Complex aggregations (monthly spend, category groupings, inflows vs outflows) execute natively on MongoDB Aggregation Pipelines to minimize network latency and memory overhead.
4. **Resilient AI Pipeline**: Pre-trained machine learning and deep learning models are serialized into `models/` using `joblib` and Keras formats for sub-5ms inference.
