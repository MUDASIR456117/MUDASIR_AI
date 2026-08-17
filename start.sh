#!/bin/bash
set -e

APP_PORT=${PORT:-8000}
echo "=============================================="
echo "Starting AI Financial Advisor on Port: $APP_PORT"
echo "=============================================="

if [ "$SERVICE_TYPE" = "frontend" ]; then
    echo "Starting Streamlit Frontend on port $APP_PORT..."
    exec streamlit run frontend/app.py --server.port=$APP_PORT --server.address=0.0.0.0 --server.headless=true
elif [ "$SERVICE_TYPE" = "backend" ]; then
    echo "Starting FastAPI Backend on port $APP_PORT..."
    exec uvicorn backend.app.main:app --host 0.0.0.0 --port=$APP_PORT
else
    echo "Starting FastAPI Backend on internal port 8000..."
    uvicorn backend.app.main:app --host 0.0.0.0 --port=8000 &
    
    echo "Starting Streamlit Frontend on public port $APP_PORT..."
    exec streamlit run frontend/app.py --server.port=$APP_PORT --server.address=0.0.0.0 --server.headless=true
fi
