#!/bin/bash
# Production start script for Render

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Install dependencies
pip install -r requirements.txt

# Start the application
uvicorn app:app --host 0.0.0.0 --port ${PORT:-8000}

