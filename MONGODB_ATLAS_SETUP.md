# 🍃 MongoDB Atlas Setup Guide

## Step-by-Step Instructions

### 1. Create MongoDB Atlas Account

1. Go to: https://www.mongodb.com/cloud/atlas/register
2. Sign up with your email (free account)
3. Verify your email

### 2. Create a Free Cluster

1. After logging in, click **"Build a Database"**
2. Choose **"M0 FREE"** tier (Free Forever)
3. Select a **Cloud Provider** (AWS, Google Cloud, or Azure)
4. Choose a **Region** closest to you
5. Name your cluster (default: "Cluster0" is fine)
6. Click **"Create"** (takes 3-5 minutes)

### 3. Create Database User

1. Go to **"Database Access"** (left sidebar)
2. Click **"Add New Database User"**
3. Choose **"Password"** authentication
4. Enter:
   - **Username**: `edulingua_user` (or your choice)
   - **Password**: Generate a secure password (save it!)
5. Set privileges to **"Read and write to any database"**
6. Click **"Add User"**

### 4. Configure Network Access

1. Go to **"Network Access"** (left sidebar)
2. Click **"Add IP Address"**
3. For development, click **"Allow Access from Anywhere"**
   - This adds `0.0.0.0/0` (all IPs)
   - ⚠️ Only for development! For production, add specific IPs
4. Click **"Confirm"**

### 5. Get Connection String

1. Go back to **"Database"** (left sidebar)
2. Click **"Connect"** on your cluster
3. Choose **"Connect your application"**
4. Select **"Python"** and version **"3.6 or later"**
5. Copy the connection string (looks like):
   ```
   mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```
6. **Replace** `<username>` and `<password>` with your database user credentials
7. **Add database name** at the end:
   ```
   mongodb+srv://edulingua_user:yourpassword@cluster0.xxxxx.mongodb.net/edulingua?retryWrites=true&w=majority
   ```

### 6. Update Backend Configuration

Update `backend/.env` with your connection string:

```env
DATABASE_URL=mongodb+srv://edulingua_user:yourpassword@cluster0.xxxxx.mongodb.net/edulingua?retryWrites=true&w=majority
DATABASE_NAME=edulingua
```

**Important**: 
- Replace `edulingua_user` with your actual username
- Replace `yourpassword` with your actual password
- Replace `cluster0.xxxxx.mongodb.net` with your actual cluster URL
- Keep `/edulingua` at the end (database name)

### 7. Test Connection

After updating `.env`, restart the backend and check the console for:
```
✅ MongoDB connected successfully
```

---

## 🔒 Security Notes

- **Never commit `.env` file to Git** (it's in .gitignore)
- For production, use specific IP whitelist instead of 0.0.0.0/0
- Rotate passwords regularly
- Use environment variables in production

---

## ✅ Verification

Once connected, you should see:
- Backend starts without MongoDB errors
- Signup/login works
- Data is saved to MongoDB Atlas

---

**Need help? Check the MongoDB Atlas documentation or see the error messages in your backend console.**
