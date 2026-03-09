@echo off
echo ============================================
echo Starting Context-Aware Agent
echo ============================================
echo.

echo This will open 2 terminal windows:
echo 1. Backend Server (FastAPI)
echo 2. Frontend Server (React + Vite)
echo.
echo Make sure you have run setup.bat first!
echo.
pause

echo Starting Backend Server...
start cmd /k "cd backend && venv\Scripts\activate && uvicorn main:app --reload"

timeout /t 3 /nobreak >nul

echo Starting Frontend Server...
start cmd /k "cd frontend && npm run dev"

echo.
echo ============================================
echo Servers are starting...
echo ============================================
echo.
echo Backend will be available at: http://localhost:8000
echo Frontend will be available at: http://localhost:5173
echo API Docs available at: http://localhost:8000/docs
echo.
echo Press any key to exit this window (servers will keep running)
pause
