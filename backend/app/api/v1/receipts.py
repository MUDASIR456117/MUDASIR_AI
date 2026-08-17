import os
import shutil
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from typing import Dict, Any
from pathlib import Path
from datetime import datetime
from backend.app.schemas.receipt import ReceiptParseResult, ReceiptResponse
from backend.app.security.dependencies import get_current_active_user
from backend.app.services.receipt_service import receipt_service
from backend.app.config import settings
from backend.app.database import get_sync_database

router = APIRouter(prefix="/receipts", tags=["Receipts Scanner"])

@router.post("/scan", response_model=ReceiptParseResult)
async def scan_receipt(
    file: UploadFile = File(...),
    current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    """Upload receipt (JPG, PNG, PDF), run OpenCV image preprocessing, and extract structured data."""
    ext = Path(file.filename).suffix.lower()
    if ext not in [".jpg", ".jpeg", ".png", ".pdf"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported file format. Please upload JPG, PNG, or PDF receipt."
        )

    receipt_dir = Path(settings.UPLOAD_DIR) / "receipts"
    receipt_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    saved_filename = f"{current_user['id']}_{timestamp}_{file.filename}"
    file_path = receipt_dir / saved_filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        raw_text = receipt_service.extract_text_from_file(str(file_path))
        parsed = receipt_service.parse_receipt_data(raw_text)

        sync_db = get_sync_database()
        if sync_db is not None:
            sync_db.receipts.insert_one({
                "user_id": current_user["id"],
                "filename": file.filename,
                "file_path": str(file_path),
                "parsed_data": parsed,
                "created_at": datetime.utcnow()
            })

        return parsed
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"OCR processing failed: {str(e)}")
