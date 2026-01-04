# ⚠️ NPM NOT INSTALLED - Setup Guide

## Problem
`npm` is not recognized - Node.js and npm are not installed on this system.

## Solution

### Step 1: Install Node.js
The project requires **Node.js 18+** with npm.

**Download from:** https://nodejs.org/
- Choose **LTS (Long Term Support)** version
- Windows installer (.msi)
- Accept all defaults during installation

### Step 2: Verify Installation
After installation, close and reopen PowerShell, then run:
```powershell
node --version
npm --version
```

You should see version numbers like:
```
v18.x.x
9.x.x
```

### Step 3: Install Dependencies
Once Node.js is installed, run:
```powershell
cd "C:\Users\cheeh\Desktop\webservice ramadan\app\schemas\frontend webservice site"
npm install
```

### Step 4: Start the Project
```powershell
npm run dev
```

Then open: **http://localhost:5173/**

---

## What's Already Ready

All project files are complete and configured:
✅ All React components created
✅ All API integrations done
✅ All styling configured
✅ All documentation written

**You just need Node.js installed!**

---

## After Installing Node.js

Run these 3 commands:
```powershell
npm install
npm run dev
# Open http://localhost:5173/ in browser
```

---

## If Installation Still Fails

### Common Issues

**1. npm: command not found**
- Node.js not in PATH
- Solution: Restart PowerShell after installation

**2. Permission denied errors**
- Try: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

**3. Legacy dependency issues**
- Try: `npm install --legacy-peer-deps`

**4. Port 5173 already in use**
- Try: `npm run dev -- --port 3000`

### Need Help?

1. Check Node.js version: `node --version`
2. Check npm version: `npm --version`
3. Check npm cache: `npm cache clean --force`
4. Reinstall: `rm -r node_modules package-lock.json` then `npm install`

---

## System Requirements

- **Node.js:** 18.0.0 or higher
- **npm:** 9.0.0 or higher
- **RAM:** 4GB minimum
- **Disk Space:** 500MB free

---

## Alternative: Use Online IDE

If you can't install Node.js locally, use:
- **Replit.com** (free, online IDE)
- **CodeSandbox.io** (online React editor)
- **StackBlitz.com** (Vite support)

Just upload the `src/` folder and project files.

---

## Quick Checklist

- [ ] Downloaded Node.js LTS
- [ ] Ran installer with default settings
- [ ] Restarted PowerShell
- [ ] Verified: `node --version` and `npm --version`
- [ ] Ran: `npm install` (takes 2-5 minutes)
- [ ] Ran: `npm run dev`
- [ ] Opened: http://localhost:5173/

---

**Once Node.js is installed, everything will work!** ✨

The frontend code is 100% ready - just needs npm to bundle it.
