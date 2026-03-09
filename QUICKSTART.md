# Quick Start Guide

Get up and running in 5 minutes!

## Prerequisites

- ✅ Python 3.9+ installed
- ✅ Node.js 18+ installed
- ✅ OpenAI API Key ([Get one here](https://platform.openai.com/api-keys))

## 🚀 Quick Setup (Windows)

### Option 1: Automated Setup (Recommended)

```bash
# Run the setup script
setup.bat

# Edit backend/.env and add your OpenAI API key
notepad backend\.env

# Start both servers
start.bat
```

### Option 2: Manual Setup

```bash
# Backend Setup
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
notepad .env  # Add your OpenAI API key
python create_pdf.py

# Frontend Setup (in new terminal)
cd frontend
npm install
npm run dev
```

## 🎯 Run the Application

### Terminal 1 - Backend
```bash
cd backend
venv\Scripts\activate
uvicorn main:app --reload
```
**Backend runs at:** http://localhost:8000

### Terminal 2 - Frontend
```bash
cd frontend
npm run dev
```
**Frontend runs at:** http://localhost:5173

## ✅ Test It

1. Open http://localhost:5173 in your browser
2. Try asking: **"What did we decide about the logistics?"**
3. Check the **Reminders panel** on the right
4. View API docs at: http://localhost:8000/docs

## 🔑 Environment Setup

### backend/.env
```env
OPENAI_API_KEY=sk-your-actual-key-here
```

⚠️ **IMPORTANT**: You MUST add your OpenAI API key for the system to work!

## 💡 Sample Queries

Try these in the chat:

- "What did we decide about the event logistics?"
- "When is the next meeting?"
- "What is the venue address?"
- "Show me all upcoming events"
- "Who is handling the catering?"

## 🔍 Verify Everything Works

### Check Backend
```bash
curl http://localhost:8000/
```
Should return: `{"status":"running",...}`

### Check Frontend
Open browser to http://localhost:5173

### Check Data Files
```bash
dir backend\data
```
Should show:
- emails.txt ✅
- events.csv ✅
- notes.pdf ✅ (or notes_text_version.txt)

## 🐛 Troubleshooting

### "OPENAI_API_KEY not set"
➡️ Edit `backend/.env` and add your API key

### "Module not found"
➡️ Run `pip install -r requirements.txt` in backend with venv activated

### Frontend won't load
➡️ Run `npm install` in frontend directory

### Backend crashes on startup
➡️ Check Python version: `python --version` (need 3.9+)

## 🎉 You're Done!

The system is now running with:
- ✅ FastAPI backend with AI agent
- ✅ React frontend with chat interface
- ✅ Multi-source search (email, PDF, CSV)
- ✅ Calendar integration with reminders
- ✅ FAISS vector database for semantic search

## 📚 Next Steps

1. **n8n Automation** - See main README.md
2. **Customize Data** - Edit files in `backend/data/`
3. **Add Events** - Update `backend/data/events.csv`
4. **Explore API** - Visit http://localhost:8000/docs

---

**Need help?** Check the main [README.md](README.md) for detailed documentation.
