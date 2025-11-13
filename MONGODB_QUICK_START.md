# 🍃 MongoDB Quick Start

## ⚠️ MongoDB is Required

The application requires MongoDB to be running for user authentication and data storage.

## 🚀 Quick Setup Options

### Option 1: Install MongoDB Locally (macOS)

```bash
# Install MongoDB
brew tap mongodb/brew
brew install mongodb-community

# Start MongoDB
brew services start mongodb-community

# Verify it's running
mongosh
```

### Option 2: Use MongoDB Atlas (Cloud - Recommended)

1. **Sign up** at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) (free tier available)
2. **Create a cluster** (free M0 tier works)
3. **Get connection string**:
   - Click "Connect" on your cluster
   - Choose "Connect your application"
   - Copy the connection string
4. **Update `backend/.env`**:
   ```env
   DATABASE_URL=mongodb+srv://username:password@cluster.mongodb.net/
   DATABASE_NAME=edulingua
   ```
5. **Whitelist your IP** in Atlas Network Access (or use 0.0.0.0/0 for development)

### Option 3: Docker (if you have Docker)

```bash
docker run -d -p 27017:27017 --name mongodb mongo:latest
```

## ✅ Verify MongoDB is Running

```bash
# Test connection
mongosh

# Or test from Python
python -c "from motor.motor_asyncio import AsyncIOMotorClient; import asyncio; asyncio.run(AsyncIOMotorClient('mongodb://localhost:27017').admin.command('ping')); print('✅ MongoDB is running!')"
```

## 🔧 Update Environment

Make sure `backend/.env` has:
```env
DATABASE_URL=mongodb://localhost:27017
DATABASE_NAME=edulingua
```

For Atlas:
```env
DATABASE_URL=mongodb+srv://username:password@cluster.mongodb.net/
DATABASE_NAME=edulingua
```

## 🎯 After MongoDB is Running

1. **Restart the backend**:
   ```bash
   cd backend
   source venv/bin/activate
   uvicorn app:app --reload --port 8000
   ```

2. **Try signing up again** at http://localhost:5173

---

**Once MongoDB is running, the application will work perfectly! 🚀**
