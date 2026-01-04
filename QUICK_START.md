# 🚀 Ramadan Helper - Complete Startup Guide

## ✅ What You Have:
- ✅ PostgreSQL installed
- ✅ YouTube API Key: `AIzaSyCPENCj8Er50HzFLwhYPG9rH_AsCMo4_qI`
- ✅ Backend code (FastAPI)
- ✅ Frontend code (HTML with API integration)

---

## 📝 STEP 1: Set Up PostgreSQL Database

### Option A: Using pgAdmin (Easiest)
1. Open **pgAdmin** (comes with PostgreSQL)
2. Right-click on **Databases** → **Create** → **Database**
3. Name: `ramadan_db`
4. Owner: `postgres`
5. Click **Save**

### Option B: Using Command Line
1. Open **Command Prompt** or **PowerShell**
2. Run:
```bash
psql -U postgres
```
3. Enter your PostgreSQL password
4. Copy-paste this command:
```sql
CREATE DATABASE ramadan_db;
```
5. Press Enter, then type `\q` to exit

**Note:** If you get "psql not found", add PostgreSQL to PATH or navigate to PostgreSQL bin folder:
```bash
cd "C:\Program Files\PostgreSQL\15\bin"
psql -U postgres
```

---

## 🔧 STEP 2: Start the Backend

### 2.1 Open Terminal in Backend Folder
```bash
cd C:\Users\cheeh\Desktop\webservice ramadan\backend
```

### 2.2 Run Setup Script
```bash
setup.bat
```

This will:
- Create Python virtual environment
- Install all dependencies
- Show you next steps

### 2.3 Start Backend Server
```bash
python main.py
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

✅ **Backend is running!**

---

## 📺 STEP 3: Add Videos to Database

### 3.1 Open API Documentation
In your browser: **http://localhost:8000/docs**

### 3.2 Search YouTube for Videos

1. Find the `POST /api/search/youtube` endpoint
2. Click **Try it out**
3. Enter query:
```json
{
  "query": "Ramadan Islamic lecture prayer taraweeh",
  "max_results": 5
}
```
4. Click **Execute**
5. Copy the `videoId` values from results (look for `"videoId": "xxxxx"`)

### 3.3 Import Videos to Database

1. Find `POST /api/videos/import` endpoint
2. Click **Try it out**
3. Add keywords as parameters:
   - Click **+ keyword**
   - Add: `ramadan`, `islam`, `prayer`, `lecture`
4. In body, paste:
```json
{
  "youtube_ids": ["copy_video_ids_here"]
}
```

**Example:**
```json
{
  "youtube_ids": ["dQw4w9WgXcQ", "jNQXAC9IVRw", "ZbZSe6N_BXs"]
}
```

5. Click **Execute**
6. You should see videos imported successfully ✅

**Repeat this process to add more videos!**

---

## 🎯 STEP 4: Test the Frontend

### 4.1 Open Frontend
Open `app.html` in your browser:
```
C:\Users\cheeh\Desktop\webservice ramadan\app\schemas\frontend webservice site\app.html
```

Double-click the file or drag it to your browser.

### 4.2 Test Islamic Videos Feature
1. Click **📺 Islamic Videos** in the menu
2. Type a problem: `"I'm struggling with concentration during prayer"`
3. Click **🔍 Find Relevant Video**
4. You should see results from your database! ✅

---

## 🐛 Troubleshooting

### "Connection refused" or "Cannot connect to API"
**Problem:** Backend is not running
**Solution:**
```bash
cd backend
python main.py
```
Make sure you see "Uvicorn running on http://127.0.0.1:8000"

### "No videos found" in search
**Problem:** Database is empty
**Solution:** Follow Step 3 to import videos

### "YOUTUBE_API_KEY" error
**Problem:** API key not in .env file
**Solution:** Check `backend/.env` has:
```
YOUTUBE_API_KEY=AIzaSyCPENCj8Er50HzFLwhYPG9rH_AsCMo4_qI
DATABASE_URL=postgresql://postgres:password@localhost:5432/ramadan_db
```

### "Database connection failed"
**Problem:** PostgreSQL not running
**Solution:**
1. Open Services (Windows key + Services)
2. Find "PostgreSQL" service
3. Click **Start** if stopped
4. Or use pgAdmin to verify connection

### YouTube API quota exceeded
**Problem:** Too many API requests
**Solution:** Wait a few hours, or use already-imported videos

---

## 📊 API Endpoints Quick Reference

```
GET  /api/videos              - List all videos
POST /api/search              - Search videos by query
POST /api/search/youtube      - Search YouTube (for import)
POST /api/videos/import       - Import videos from YouTube
POST /api/users              - Create/get user
```

Full docs: http://localhost:8000/docs

---

## 🎓 Next Steps

1. **Import more videos** - Add 20-50 Islamic videos for better search results
2. **Test search** - Try different search queries to verify relevance
3. **Deploy backend** - Host on Heroku/AWS/DigitalOcean
4. **Update frontend** - Change `API_BASE_URL` to production server
5. **Add user authentication** - Secure user accounts

---

## ⚙️ Database Info

**Database Name:** `ramadan_db`
**Server:** `localhost:5432`
**Username:** `postgres`
**Tables Created Automatically:**
- videos
- keywords
- users
- searches
- search_results
- saved_videos
- video_keywords

**Connect manually:**
```bash
psql -U postgres -d ramadan_db
```

---

## 💡 Tips

1. **Keep backend running** - Leave terminal open while testing
2. **Check console errors** - Backend terminal shows API errors
3. **Browser console** - Press F12 to see frontend errors
4. **Clear browser cache** - Sometimes helps with API issues
5. **API docs are interactive** - Use /docs to test all endpoints

---

## 📞 Quick Commands

```bash
# Start backend
cd backend && python main.py

# Connect to database
psql -U postgres -d ramadan_db

# View backend logs
# (Just look at terminal running main.py)

# Kill backend server
# (Ctrl+C in terminal)
```

---

**You're all set! 🎉 Start by running the backend and adding some videos!**
