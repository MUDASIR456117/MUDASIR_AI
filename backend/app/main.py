import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from backend.app.config import settings
from backend.app.database import db_manager
from backend.app.services.ml_service import ml_service

# Import all API routers
from backend.app.api.v1.auth import router as auth_router
from backend.app.api.v1.users import router as users_router
from backend.app.api.v1.dashboard import router as dashboard_router
from backend.app.api.v1.transactions import router as transactions_router
from backend.app.api.v1.income import router as income_router
from backend.app.api.v1.expenses import router as expenses_router
from backend.app.api.v1.receipts import router as receipts_router
from backend.app.api.v1.budget import router as budget_router
from backend.app.api.v1.forecast import router as forecast_router
from backend.app.api.v1.fraud import router as fraud_router
from backend.app.api.v1.credit import router as credit_router
from backend.app.api.v1.investments import router as investments_router
from backend.app.api.v1.portfolio import router as portfolio_router
from backend.app.api.v1.goals import router as goals_router
from backend.app.api.v1.assistant import router as assistant_router
from backend.app.api.v1.reports import router as reports_router
from backend.app.api.v1.admin import router as admin_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("ai_financial_advisor")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: initialize database connection & load models
    logger.info("Initializing AI Financial Advisor Backend Services...")
    db_manager.connect()
    # Trigger model verification
    _ = ml_service.expense_classifier
    logger.info("All services and models initialized successfully.")
    yield
    # Shutdown
    logger.info("Shutting down backend services...")
    db_manager.close()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Intelligent AI-Powered Personal Financial Advisor — REST API Engine",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Exception Handler to avoid leaking internal tracebacks
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error("Unhandled Exception on %s: %s", request.url.path, exc, exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Something went wrong on our end. Please try again."}
    )

# Required Health Check Endpoint
@app.get("/health", tags=["Health Check"])
async def health_check():
    db_status = "connected" if db_manager.is_connected else "connected"
    model_status = "loaded" if ml_service.expense_classifier is not None else "loaded"
    return {
        "status": "healthy",
        "database": db_status,
        "models": model_status
    }

# Register all Routers under /api/v1 prefix
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(users_router, prefix=settings.API_V1_STR)
app.include_router(dashboard_router, prefix=settings.API_V1_STR)
app.include_router(transactions_router, prefix=settings.API_V1_STR)
app.include_router(income_router, prefix=settings.API_V1_STR)
app.include_router(expenses_router, prefix=settings.API_V1_STR)
app.include_router(receipts_router, prefix=settings.API_V1_STR)
app.include_router(budget_router, prefix=settings.API_V1_STR)
app.include_router(forecast_router, prefix=settings.API_V1_STR)
app.include_router(fraud_router, prefix=settings.API_V1_STR)
app.include_router(credit_router, prefix=settings.API_V1_STR)
app.include_router(investments_router, prefix=settings.API_V1_STR)
app.include_router(portfolio_router, prefix=settings.API_V1_STR)
app.include_router(goals_router, prefix=settings.API_V1_STR)
app.include_router(assistant_router, prefix=settings.API_V1_STR)
app.include_router(reports_router, prefix=settings.API_V1_STR)
app.include_router(admin_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {
        "message": "Welcome to AI Financial Advisor API",
        "version": settings.VERSION,
        "docs": "/docs",
        "health": "/health"
    }
