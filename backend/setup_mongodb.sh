#!/bin/bash

echo "🍃 MongoDB Setup Helper for EduLingua Pro"
echo "=========================================="
echo ""

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cat > .env << 'EOF'
# MongoDB Configuration
# For MongoDB Atlas (Cloud) - REPLACE WITH YOUR CONNECTION STRING:
DATABASE_URL=mongodb+srv://username:password@cluster.mongodb.net/edulingua?retryWrites=true&w=majority
DATABASE_NAME=edulingua

# For Local MongoDB:
# DATABASE_URL=mongodb://localhost:27017
# DATABASE_NAME=edulingua

# JWT Secret Key
SECRET_KEY=edulingua-pro-secret-key-change-in-production-min-32-characters-long

# API Configuration
API_V1_PREFIX=
CORS_ORIGINS=["http://localhost:5173","http://localhost:3000","http://127.0.0.1:5173"]
EOF
    echo "✅ Created .env file"
    echo ""
    echo "⚠️  IMPORTANT: Update DATABASE_URL in .env with your MongoDB Atlas connection string!"
    echo ""
else
    echo "✅ .env file already exists"
    echo ""
fi

# Test connection
echo "🔍 Testing MongoDB connection..."
source venv/bin/activate
python test_mongodb_connection.py

echo ""
echo "📋 Next steps:"
echo "   1. If connection failed, update DATABASE_URL in .env"
echo "   2. Run this script again to test: ./setup_mongodb.sh"
echo "   3. Once connection works, restart the backend server"
