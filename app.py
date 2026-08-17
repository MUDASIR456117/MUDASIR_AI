import sys
import os
from pathlib import Path

# Add project root to sys.path
_ROOT = str(Path(__file__).resolve().parent)
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

# Load and execute frontend/app.py
frontend_app_path = Path(__file__).resolve().parent / "frontend" / "app.py"
with open(frontend_app_path, "r", encoding="utf-8") as f:
    exec(f.read(), globals())
