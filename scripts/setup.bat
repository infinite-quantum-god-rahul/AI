@echo off
REM AI Resume Analyzer Setup Script for Windows
REM This script sets up the development environment

echo 🚀 Setting up AI Resume Analyzer ^& Job Matching Platform...

REM Check if Python is installed
echo [INFO] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python 3.11+ is required but not installed
    exit /b 1
)
python --version
echo [SUCCESS] Python is installed

REM Check if Node.js is installed
echo [INFO] Checking Node.js installation...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js 18+ is required but not installed
    exit /b 1
)
node --version
echo [SUCCESS] Node.js is installed

REM Check if Docker is installed
echo [INFO] Checking Docker installation...
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] Docker is not installed. You can still run in development mode
) else (
    docker --version
    echo [SUCCESS] Docker is installed
)

REM Create virtual environment
echo [INFO] Setting up Python virtual environment...
if not exist "venv" (
    python -m venv venv
    echo [SUCCESS] Virtual environment created
) else (
    echo [INFO] Virtual environment already exists
)

REM Activate virtual environment
call venv\Scripts\activate.bat
echo [SUCCESS] Virtual environment activated

REM Install Python dependencies
echo [INFO] Installing Python dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt
echo [SUCCESS] Python dependencies installed

REM Download spaCy model
echo [INFO] Downloading spaCy English model...
python -m spacy download en_core_web_sm
echo [SUCCESS] spaCy model downloaded

REM Install Node.js dependencies
echo [INFO] Installing Node.js dependencies...
npm install
echo [SUCCESS] Node.js dependencies installed

REM Create necessary directories
echo [INFO] Creating necessary directories...
if not exist "uploads" mkdir uploads
if not exist "logs" mkdir logs
if not exist "ssl" mkdir ssl
echo [SUCCESS] Directories created

REM Set up environment file
echo [INFO] Setting up environment configuration...
if not exist ".env" (
    copy env.example .env
    echo [SUCCESS] Environment file created from template
    echo [WARNING] Please edit .env file with your configuration
) else (
    echo [INFO] Environment file already exists
)

REM Initialize database
echo [INFO] Initializing database...
python -c "from backend.database import init_db, create_sample_data; init_db(); create_sample_data(); print('Database initialized successfully')"
if %errorlevel% neq 0 (
    echo [WARNING] Database initialization failed. Please ensure PostgreSQL is running and configured correctly
)

REM Build frontend
echo [INFO] Building frontend...
npm run build
echo [SUCCESS] Frontend built successfully

echo.
echo 🎉 Setup completed successfully!
echo.
echo Next steps:
echo 1. Edit .env file with your configuration
echo 2. Start the backend: cd backend ^&^& python main.py
echo 3. Start the frontend: npm run dev
echo 4. Or use Docker: docker-compose up -d
echo.
echo Access the application:
echo - Frontend: http://localhost:3000
echo - Backend API: http://localhost:8000
echo - API Docs: http://localhost:8000/docs
echo.

pause
