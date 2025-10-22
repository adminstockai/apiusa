#!/bin/bash

cd "$(dirname "$0")"

echo "============================================================"
echo "Stock Analysis Landing Page - Backend Server"
echo "============================================================"
echo ""

echo "Installing dependencies..."
python3 -m pip install -r requirements.txt -q 2>/dev/null || echo "Dependencies already installed or pip not available"
echo ""

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DB_PATH="$SCRIPT_DIR/data/app.db"

if [ ! -f "$DB_PATH" ]; then
    echo "Database not found at: $DB_PATH"
    echo "Initializing database..."
    python3 init_db.py
    echo ""
else
    echo "Database found at: $DB_PATH"
    echo ""
fi

echo "Starting FastAPI server..."
echo "The database will be auto-initialized if needed..."
echo ""
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
