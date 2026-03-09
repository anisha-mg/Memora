@echo off
echo ============================================
echo Context-Aware Agent - Quick Setup Script
echo ============================================
echo.

echo Step 1: Setting up Backend...
cd backend

echo Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    echo Make sure Python 3.9+ is installed
    pause
    exit /b 1
)

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing Python dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo Creating .env file...
if not exist .env (
    copy .env.example .env
    echo .env file created - PLEASE EDIT IT AND ADD YOUR OPENAI API KEY!
) else (
    echo .env file already exists
)

echo.
echo Generating sample PDF...
python create_pdf.py

cd ..

echo.
echo Step 2: Setting up Frontend...
cd frontend

echo Installing Node dependencies...
call npm install
if errorlevel 1 (
    echo ERROR: Failed to install Node dependencies
    echo Make sure Node.js is installed
    pause
    exit /b 1
)

echo.
echo Creating frontend .env file...
if not exist .env (
    copy .env.example .env
    echo Frontend .env file created
) else (
    echo Frontend .env file already exists
)

cd ..

echo.
echo ============================================
echo Setup Complete!
echo ============================================
echo.
echo IMPORTANT: Edit backend/.env and add your OpenAI API key!
echo.
echo To start the application:
echo 1. Backend:  cd backend ^&^& venv\Scripts\activate ^&^& uvicorn main:app --reload
echo 2. Frontend: cd frontend ^&^& npm run dev
echo.
echo For n8n automation:
echo 1. Install: npm install -g n8n
echo 2. Start: n8n start
echo 3. Import: n8n/reminder_workflow.json
echo.
pause
