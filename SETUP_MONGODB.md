# 🍃 MongoDB Setup - Quick Start

## 🚀 Option 1: MongoDB Atlas (Recommended - 5 minutes)

### Step 1: Create Account & Cluster
1. Go to: **https://www.mongodb.com/cloud/atlas/register**
2. Sign up (free)
3. Create **M0 FREE** cluster
4. Wait 3-5 minutes for cluster to deploy

### Step 2: Configure Access
1. **Database Access** → Add user:
   - Username: `edulingua_user`
   - Password: (generate secure password, save it!)
   - Privileges: Read and write to any database

2. **Network Access** → Add IP:
   - Click "Allow Access from Anywhere" (0.0.0.0/0)
   - ⚠️ Development only!

### Step 3: Get Connection String
1. **Database** → Click "Connect" on your cluster
2. Choose **"Connect your application"**
3. Copy the connection string
4. Replace `<username>` and `<password>` with your credentials
5. Add database name: `/edulingua` before `?retryWrites`

**Example:**
```
mongodb+srv://edulingua_user:YourPassword123@cluster0.xxxxx.mongodb.net/edulingua?retryWrites=true&w=majority
```

### Step 4: Configure Backend

Run the setup script:
```bash
cd backend
./setup_mongodb.sh
```

Or manually create `backend/.env`:
```env
DATABASE_URL=mongodb+srv://edulingua_user:YourPassword123@cluster0.xxxxx.mongodb.net/edulingua?retryWrites=true&w=majority
DATABASE_NAME=edulingua
SECRET_KEY=your-secret-key-change-in-production
CORS_ORIGINS=["http://localhost:5173","http://localhost:3000"]
```

### Step 5: Test Connection
```bash
cd backend
source venv/bin/activate
python test_mongodb_connection.py
```

You should see: `✅ MongoDB connection successful!`

### Step 6: Restart Backend
```bash
cd backend
source venv/bin/activate
uvicorn app:app --reload --port 8000
```

Look for: `✅ MongoDB connected successfully`

---

## 🐳 Option 2: Docker (If you have Docker)

```bash
# Start MongoDB container
docker run -d -p 27017:27017 --name mongodb mongo:latest

# Update backend/.env
DATABASE_URL=mongodb://localhost:27017
DATABASE_NAME=edulingua

# Test connection
cd backend
source venv/bin/activate
python test_mongodb_connection.py
```

---

## 💻 Option 3: Install MongoDB Locally

### macOS
```bash
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community
```

### Linux (Ubuntu/Debian)
```bash
sudo apt-get install -y mongodb
sudo systemctl start mongod
```

Then update `backend/.env`:
```env
DATABASE_URL=mongodb://localhost:27017
DATABASE_NAME=edulingua
```

---

## ✅ Verify Everything Works

1. **Test connection**: `python backend/test_mongodb_connection.py`
2. **Start backend**: `uvicorn app:app --reload --port 8000`
3. **Check console**: Should see `✅ MongoDB connected successfully`
4. **Try signup**: Go to http://localhost:5173 and sign up
5. **Check Atlas**: Go to Atlas → Database → Browse Collections to see your data!

---

## 🎯 Quick Command Reference

```bash
# Test MongoDB connection
cd backend && source venv/bin/activate && python test_mongodb_connection.py

# Start backend
cd backend && source venv/bin/activate && uvicorn app:app --reload --port 8000

# Start frontend
cd frontend && npm run dev
```

---

**Once MongoDB is connected, your application is fully functional! 🚀**
