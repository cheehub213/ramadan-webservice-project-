# 🗄️ Database Connection Error - FIX

## Problem

The backend tried to start but **PostgreSQL database is not running!**

Error message:
```
psycopg2.OperationalError: connection to server at "localhost" (::1), port 5432 failed
Is the server running on that host and accepting TCP/IP connections?
```

---

## ✅ Solution: Start PostgreSQL

### **On Windows** ⭐ (Recommended)

#### Step 1: Open Windows Services
1. Press: **Windows Key + R**
2. Type: `services.msc`
3. Press: **Enter**

#### Step 2: Find PostgreSQL
- Look in the list for: **PostgreSQL** (or **postgresql-x64-15**)
- If you don't see it, search at the top

#### Step 3: Start the Service
1. Right-click on PostgreSQL
2. Select: **Start**
3. Wait **10-15 seconds** for it to fully start
4. Status should change to "Running" (green arrow)

#### Step 4: Run Backend Again
```bash
cd C:\Users\cheeh\Desktop\webservice ramadan\backend
python main.py
```

---

### **Alternative: Command Line Method**

Open PowerShell as Administrator and run:
```powershell
net start PostgreSQL15
```

Replace `15` with your PostgreSQL version if different.

---

### **On Mac/Linux**

```bash
# Using Homebrew
brew services start postgresql

# Or using systemctl
sudo systemctl start postgresql
```

---

## ✅ How to Know If PostgreSQL is Running

### Windows:
- Go to **Services** (services.msc)
- Find PostgreSQL
- Status shows: ✅ **Running** (green)

### Command Line (All):
```bash
psql --version
```
If you see a version number, PostgreSQL is installed.

```bash
psql -U postgres -c "SELECT 1"
```
If you see `1` as result, PostgreSQL is running!

---

## 🔄 Steps to Get Backend Running

1. **START POSTGRESQL** ← You are here
   - [ ] Open services.msc
   - [ ] Find PostgreSQL
   - [ ] Click Start
   - [ ] Wait 10-15 seconds
   - [ ] Verify it's "Running"

2. **RUN BACKEND**
   - [ ] Go to: `C:\Users\cheeh\Desktop\webservice ramadan\backend`
   - [ ] Run: `python main.py`
   - [ ] Wait for: "Uvicorn running on http://127.0.0.1:8000"

3. **TEST CONNECTION**
   - [ ] Open frontend in browser
   - [ ] Go to 📺 **Islamic Videos**
   - [ ] Click **Check Backend Status**
   - [ ] Should show: ✅ Backend Running

4. **USE THE APP**
   - [ ] Search for videos
   - [ ] Import YouTube videos (optional)
   - [ ] Enjoy!

---

## 🆘 Still Having Issues?

### PostgreSQL won't start?
1. Check if PostgreSQL is installed
2. Try restarting your computer
3. Check Windows Event Viewer for error messages

### Can't find PostgreSQL service?
1. You may not have PostgreSQL installed
2. Install from: https://www.postgresql.org/download/windows/
3. Run installer and complete setup

### Port 5432 already in use?
1. Check if another PostgreSQL instance is running
2. Or check if another service is using port 5432
3. Command: `netstat -ano | findstr :5432`

---

## 📝 Remember

**PostgreSQL must be running before you start the backend!**

```
PostgreSQL ✅ → Backend ✅ → Frontend ✅ → App Works! ✅
```

---

**Once PostgreSQL is running, come back and run: `python main.py`**
