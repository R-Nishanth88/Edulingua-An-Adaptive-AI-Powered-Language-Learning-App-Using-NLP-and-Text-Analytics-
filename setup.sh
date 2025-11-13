#!/bin/bash

echo "🧩 EduLingua Pro Setup Script"
echo "=============================="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9+ first."
    exit 1
fi

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+ first."
    exit 1
fi

echo "✅ Python and Node.js are installed"
echo ""

# Backend setup
echo "📦 Setting up backend..."
cd backend

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate
echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Downloading spaCy model..."
python -m spacy download en_core_web_sm

echo "✅ Backend setup complete!"
echo ""

# Frontend setup
cd ../frontend
echo "📦 Setting up frontend..."
npm install

echo "✅ Frontend setup complete!"
echo ""

cd ..

echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Create a MySQL database named 'edulingua'"
echo "2. Update backend/.env with your database credentials"
echo "3. Start backend: cd backend && source venv/bin/activate && uvicorn app:app --reload"
echo "4. Start frontend: cd frontend && npm run dev"
echo ""
echo "For detailed instructions, see README.md"
