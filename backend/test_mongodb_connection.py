#!/usr/bin/env python3
"""
Test MongoDB connection script.
Run this to verify your MongoDB connection string works.
"""
import asyncio
import sys
from motor.motor_asyncio import AsyncIOMotorClient
from config import settings

async def test_connection():
    """Test MongoDB connection"""
    print("🔍 Testing MongoDB connection...")
    print(f"   URL: {settings.DATABASE_URL}")
    print(f"   Database: {settings.DATABASE_NAME}")
    print()
    
    try:
        client = AsyncIOMotorClient(settings.DATABASE_URL, serverSelectionTimeoutMS=5000)
        
        # Test connection
        await client.admin.command('ping')
        print("✅ MongoDB connection successful!")
        
        # List databases
        db_list = await client.list_database_names()
        print(f"✅ Available databases: {', '.join(db_list)}")
        
        # Check if our database exists
        db = client[settings.DATABASE_NAME]
        collections = await db.list_collection_names()
        print(f"✅ Database '{settings.DATABASE_NAME}' exists")
        if collections:
            print(f"   Collections: {', '.join(collections)}")
        else:
            print("   (No collections yet - will be created on first use)")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print()
        print("💡 Troubleshooting:")
        print("   1. Check your DATABASE_URL in .env")
        print("   2. For Atlas: Verify network access allows your IP (0.0.0.0/0 for dev)")
        print("   3. For Atlas: Verify username/password are correct")
        print("   4. For local: Ensure MongoDB is running (mongosh to test)")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_connection())
    sys.exit(0 if success else 1)
