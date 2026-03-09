# Context-Aware Personal Executive – AI Memory Layer Agent

A full-stack AI-powered personal assistant that retrieves information from multiple sources and proactively sends reminders.

![System Architecture](https://img.shields.io/badge/Frontend-React%20%2B%20Vite-blue)
![Backend](https://img.shields.io/badge/Backend-FastAPI%20%2B%20Python-green)
![AI](https://img.shields.io/badge/AI-OpenAI%20%2B%20LangChain-purple)
![Automation](https://img.shields.io/badge/Automation-n8n-orange)

## 🌟 Features

### Reactive Mode
User asks questions and the AI retrieves answers from stored data:
- **Email Search**: "What did we decide about the logistics?"
- **Calendar Queries**: "When is the next meeting?"
- **Document Search**: "Summarize the logistics decisions"
- **Multi-source Search**: Searches across emails, PDFs, CSV, and calendar

### Proactive Mode
AI automatically checks calendar events and sends reminders:
- Automated reminder checks (configurable interval)
- Smart notification system
- Example: "Reminder: Logistics meeting tomorrow at 10 AM. Venue: City Convention Hall."

## 🏗️ System Architecture

```
┌─────────────────┐
│  React Frontend │
│  (Vite + Tailwind)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  FastAPI Backend │
│  /ask, /events  │
└────────┬────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌────────┐  ┌──────────────┐
│OpenAI  │  │ FAISS Vector │
│Agent   │  │ Database     │
└────────┘  └──────────────┘
    │
    ▼
┌─────────────────────────────┐
│  Data Sources               │
│  • emails.txt               │
│  • notes.pdf                │
│  • events.csv               │
└─────────────────────────────┘

┌──────────────┐
│ n8n Workflow │ ──► Automated Reminders
└──────────────┘
```

## 📁 Project Structure

```
context-aware-agent/
│
├── frontend/                    # React + Vite frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatBox.jsx     # Main chat interface
│   │   │   ├── MessageBubble.jsx  # Message display
│   │   │   └── ReminderPanel.jsx  # Reminders & events
│   │   ├── pages/
│   │   │   └── Dashboard.jsx   # Main dashboard page
│   │   ├── services/
│   │   │   └── api.js          # API service layer
│   │   ├── App.jsx             # Root component
│   │   ├── main.jsx            # Entry point
│   │   └── index.css           # Tailwind styles
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── .env.example
│
├── backend/                     # FastAPI backend
│   ├── main.py                 # FastAPI app & endpoints
│   ├── agent.py                # LangChain agent with OpenAI
│   ├── tools.py                # Data access tools
│   ├── vector_store.py         # FAISS vector database
│   ├── calendar_service.py     # Calendar management
│   ├── create_pdf.py           # PDF generator script
│   ├── requirements.txt        # Python dependencies
│   ├── .env.example            # Environment variables template
│   └── data/                   # Data files
│       ├── emails.txt          # Sample email data
│       ├── events.csv          # Calendar events
│       └── notes.pdf           # Sample PDF (generated)
│
├── n8n/
│   └── reminder_workflow.json  # n8n automation workflow
│
└── README.md                   # This file
```

## 🚀 Getting Started

### Prerequisites

- **Python** 3.9 or higher
- **Node.js** 18 or higher
- **OpenAI API Key** ([Get one here](https://platform.openai.com/api-keys))
- **n8n** (optional, for automation)

### Step 1: Clone and Setup

```bash
cd context-aware-agent
```

### Step 2: Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy .env.example .env  # Windows
# cp .env.example .env  # macOS/Linux

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=sk-your-key-here
```

### Step 3: Generate Sample PDF

```bash
# Optional: Generate notes.pdf
python create_pdf.py

# This will create data/notes.pdf
# If reportlab is not installed, it will create a text version instead
```

### Step 4: Start Backend Server

```bash
# Make sure you're in the backend directory with venv activated
uvicorn main:app --reload

# Server will start at http://localhost:8000
# API docs available at http://localhost:8000/docs
```

### Step 5: Frontend Setup

Open a new terminal:

```bash
cd frontend

# Install dependencies
npm install

# Create .env file (optional)
copy .env.example .env  # Windows
# cp .env.example .env  # macOS/Linux

# Start development server
npm run dev

# Frontend will start at http://localhost:5173
```

### Step 6: n8n Setup (Optional)

For automated reminders:

```bash
# Install n8n globally
npm install -g n8n

# Start n8n
n8n start

# n8n will start at http://localhost:5678
```

**Import the workflow:**
1. Open n8n at http://localhost:5678
2. Click "Import from File"
3. Select `n8n/reminder_workflow.json`
4. Activate the workflow
5. The workflow will check for reminders every hour

## 🔧 Configuration

### Backend Environment Variables

Create `backend/.env`:

```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
FRONTEND_URL=http://localhost:5173
```

### Frontend Environment Variables

Create `frontend/.env`:

```env
VITE_API_URL=http://localhost:8000
```

## 📡 API Endpoints

### POST `/ask`
Ask a question to the AI agent

**Request:**
```json
{
  "query": "What did we decide about the logistics?"
}
```

**Response:**
```json
{
  "response": "Based on the emails, you decided...",
  "sources": ["Emails", "PDF Documents"]
}
```

### GET `/events`
Get upcoming calendar events

**Response:**
```json
{
  "events": [
    {
      "event": "Logistics Meeting",
      "date": "2026-03-12",
      "time": "10:00",
      "days_until": 3
    }
  ]
}
```

### POST `/reminder`
Send a reminder notification

**Request:**
```json
{
  "event_name": "Logistics Meeting",
  "event_date": "2026-03-12",
  "event_time": "10:00",
  "details": "Venue: City Convention Hall"
}
```

### GET `/check-reminders`
Check for upcoming reminders (used by n8n)

**Response:**
```json
{
  "status": "success",
  "reminders": [...],
  "count": 2
}
```

### GET `/stats`
Get system statistics

**Response:**
```json
{
  "documents_indexed": 42,
  "upcoming_events": 5,
  "agent_status": "active"
}
```

## 🎯 Usage Examples

### Example Queries

1. **Search Emails:**
   - "What did we decide about the event logistics?"
   - "Who is handling the catering?"
   - "What is the venue address?"

2. **Calendar Queries:**
   - "When is the next meeting?"
   - "What events do I have this week?"
   - "Show me my schedule"

3. **Document Search:**
   - "Summarize the logistics decisions"
   - "What's the budget breakdown?"
   - "What are the important contacts?"

4. **Multi-source:**
   - "Tell me everything about the logistics meeting"
   - "What preparations are needed for the event?"

## 🛠️ Technology Stack

### Frontend
- **React 18** - UI library
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **Axios** - HTTP client
- **Heroicons** - Icon library

### Backend
- **Python 3.9+** - Programming language
- **FastAPI** - Web framework
- **OpenAI API** - LLM capabilities
- **LangChain** - Agent framework
- **FAISS** - Vector database
- **PyPDF2** - PDF processing
- **Pandas** - Data manipulation
- **Uvicorn** - ASGI server

### Automation
- **n8n** - Workflow automation

## 📊 How It Works

### Reactive Mode Flow

```
User Query → Frontend → Backend API
                ↓
        Agent (OpenAI)
                ↓
        Decides which tool to use
                ↓
    ┌───────────┴───────────┐
    ▼           ▼           ▼
Email Tool   PDF Tool   CSV Tool
    │           │           │
    └───────────┴───────────┘
                ↓
        Vector Search (FAISS)
                ↓
        Formatted Response
                ↓
        User receives answer
```

### Proactive Mode Flow

```
n8n Schedule (Every hour)
        ↓
Check Backend API (/check-reminders)
        ↓
Get events within 24 hours
        ↓
    Any events?
    ┌───┴───┐
   YES      NO
    │       │
    ▼       ▼
Send     Log
Reminder  "No reminders"
    ↓
User notified
```

## 🔍 AI Agent Details

The agent uses **OpenAI Function Calling** to intelligently decide which tools to use:

**Available Tools:**
1. `search_email(query)` - Search email content
2. `search_pdf(query)` - Search PDF documents
3. `search_csv(query)` - Search CSV data
4. `get_calendar_events()` - Get upcoming events
5. `send_reminder()` - Create reminders

**Agent Decision Process:**
1. User asks a question
2. Agent analyzes the query
3. Agent decides which tool(s) to use
4. Tools are executed in sequence
5. Results are synthesized
6. Response is returned to user

## 🎨 Frontend Features

- **Modern Dashboard UI** with Tailwind CSS
- **Real-time Chat Interface** like ChatGPT
- **Reminder Panel** showing upcoming events
- **Responsive Design** for all screen sizes
- **Auto-refresh** for reminders (every 5 minutes)
- **Source Attribution** showing where answers came from

## 🔐 Security Notes

- Store API keys in `.env` files (never commit to git)
- Add `.env` to `.gitignore`
- Use environment variables for sensitive data
- Backend CORS is configured for localhost only

## 🐛 Troubleshooting

### Backend won't start
- Check if OpenAI API key is set in `.env`
- Verify Python version: `python --version` (should be 3.9+)
- Try: `pip install -r requirements.txt --upgrade`

### Frontend won't connect to backend
- Ensure backend is running at `http://localhost:8000`
- Check CORS settings in `main.py`
- Verify `VITE_API_URL` in frontend `.env`

### FAISS errors
- FAISS requires numpy compatibility
- Try: `pip install faiss-cpu --upgrade`
- Or use CPU version: `pip install faiss-cpu`

### No reminders appearing
- Check that events are within 24 hours
- Verify dates in `events.csv` are in the future
- Check n8n workflow is active

## 📈 Future Enhancements

- [ ] Add Google Calendar integration
- [ ] Email integration (Gmail API)
- [ ] Voice input/output
- [ ] Mobile app
- [ ] Multi-user support
- [ ] Advanced NLP for better query understanding
- [ ] Custom reminder schedules
- [ ] Notification system (email, SMS)
- [ ] Data visualization dashboard
- [ ] Export conversation history

## 📝 License

This project is for educational and demonstration purposes.

## 🤝 Contributing

Feel free to fork, modify, and use this project for your hackathon or personal projects!

## 📧 Support

For issues or questions:
1. Check the troubleshooting section
2. Review API logs in backend terminal
3. Check browser console for frontend errors
4. Verify all services are running

## 🎉 Testing the System

### Quick Test Sequence

1. **Start Backend:**
   ```bash
   cd backend
   uvicorn main:app --reload
   ```

2. **Start Frontend:**
   ```bash
   cd frontend
   npm run dev
   ```

3. **Test Queries:**
   - Open http://localhost:5173
   - Try: "What did we decide about logistics?"
   - Try: "When is the next meeting?"
   - Try: "What is the venue for the event?"

4. **Check Reminders:**
   - Look at the right panel for upcoming events
   - Events within 24 hours will show as active reminders

5. **Test API Directly:**
   - Open http://localhost:8000/docs
   - Try the `/ask` endpoint with a test query
   - Check `/events` to see calendar data

## 🔗 Quick Links

- Backend API Docs: http://localhost:8000/docs
- Frontend UI: http://localhost:5173
- n8n Dashboard: http://localhost:5678

---

**Built with ❤️ for the Hackathon**

*Powered by OpenAI, LangChain, FastAPI, React, and n8n*
