@echo off
REM Ramadan Helper - Quick Start Script for Windows

echo.
echo ========================================
echo Ramadan Helper - Backend Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from python.org
    pause
    exit /b 1
)

echo [1/5] Checking PostgreSQL...
psql --version >nul 2>&1
if %errorlevel% neq 0 (
    echo WARNING: PostgreSQL might not be in PATH
    echo Make sure PostgreSQL is running
)

echo [2/5] Creating virtual environment...
if not exist venv (
    python -m venv venv
)

echo [3/5] Activating virtual environment...
call venv\Scripts\activate.bat

echo [4/5] Installing dependencies...
pip install -r requirements.txt --quiet

echo [5/5] Setup complete!
echo.
echo ========================================
echo Next Steps:
echo ========================================
echo.
echo 1. Open PostgreSQL command line:
echo    psql -U postgres
echo.
echo 2. Create database (paste in psql):
echo    CREATE USER ramadan_user WITH PASSWORD 'secure_password_123' CREATEDB;
echo    CREATE DATABASE ramadan_db OWNER ramadan_user;
echo    GRANT ALL PRIVILEGES ON DATABASE ramadan_db TO ramadan_user;
echo.
echo 3. Verify connection works:
echo    psql -U ramadan_user -d ramadan_db
echo.
echo 4. Start backend server:
echo    python main.py
echo.
echo 5. Open API documentation:
echo    http://localhost:8000/docs
echo.
echo ========================================
echo.
pause
