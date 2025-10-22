#!/bin/bash

echo "Installing dependencies..."
python3 -m pip install -r requirements.txt -q 2>/dev/null || echo "Dependencies already installed or pip not available"

if [ ! -f "data/app.db" ]; then
    echo "Database not found. Initializing..."
    python3 init_db.py
fi

echo "Starting FastAPI server..."
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
