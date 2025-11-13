# MongoDB Setup Guide for EduLingua Pro

## ✅ Migration Complete!

The application has been successfully migrated from MySQL to MongoDB.

## 📦 What Changed

- **Database**: MySQL → MongoDB
- **ORM**: SQLAlchemy → Beanie ODM
- **Driver**: PyMySQL → Motor (async MongoDB driver)
- **Models**: SQLAlchemy models → Beanie Documents

## 🚀 Quick Start

### 1. Install MongoDB

**macOS (Homebrew)**:
```bash
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community
```

**Linux (Ubuntu/Debian)**:
```bash
sudo apt-get install -y mongodb
sudo systemctl start mongod
```

**Windows**:
Download from [MongoDB Download Center](https://www.mongodb.com/try/download/community)

**Or use MongoDB Atlas (Cloud)**:
1. Sign up at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a free cluster
3. Get your connection string

### 2. Update Environment Variables

Update `backend/.env`:
```env
DATABASE_URL=mongodb://localhost:27017
DATABASE_NAME=edulingua
SECRET_KEY=your-secret-key-here
CORS_ORIGINS=["http://localhost:5173"]
```

For MongoDB Atlas:
```env
DATABASE_URL=mongodb+srv://username:password@cluster.mongodb.net/
DATABASE_NAME=edulingua
```

### 3. Install MongoDB Dependencies

```bash
cd backend
source venv/bin/activate
pip install motor beanie pymongo
```

### 4. Start the Backend

```bash
cd backend
source venv/bin/activate
uvicorn app:app --reload --port 8000
```

## 📊 Database Collections

Collections are created automatically on first use:

- **users** - User accounts
- **progress** - User progress tracking
- **feedback_logs** - Text analysis feedback
- **xp_badges** - User achievements
- **recommendations** - Learning recommendations

## 🔍 Verify MongoDB Connection

```bash
# Check if MongoDB is running
mongosh

# Or using mongo CLI
mongo

# List databases
show dbs

# Use edulingua database
use edulingua

# Show collections
show collections
```

## 🎯 Key Differences from MySQL

1. **No migrations needed** - Collections are created automatically
2. **Flexible schema** - Documents can have different fields
3. **ObjectId instead of integers** - User IDs are now ObjectIds
4. **Async operations** - All database operations are async
5. **JSON-like documents** - Native support for nested data

## 🐛 Troubleshooting

### MongoDB not running?
```bash
# macOS
brew services start mongodb-community

# Linux
sudo systemctl start mongod

# Check status
mongosh --eval "db.adminCommand('ping')"
```

### Connection refused?
- Check if MongoDB is running: `mongosh`
- Verify DATABASE_URL in `.env`
- Check firewall settings
- For Atlas: Verify IP whitelist

### Import errors?
- Make sure all dependencies are installed: `pip install motor beanie pymongo`
- Check Python version (3.9+)

## 📝 Notes

- All database operations are now async
- User IDs are ObjectIds (strings in JSON responses)
- No need for database migrations
- Collections are created automatically on first insert

---

**Happy coding with MongoDB! 🍃**
