"""
Context-Aware Personal Executive - Main FastAPI Application
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import uvicorn
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from agent import ContextAwareAgent
from calendar_service import CalendarService
from vector_store import VectorStore

app = FastAPI(title="Context-Aware Personal Executive API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:5175", "http://localhost:3000", "http://127.0.0.1:5173", "http://127.0.0.1:5174", "http://127.0.0.1:5175"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
vector_store = None
agent = None
calendar_service = None


class QueryRequest(BaseModel):
    query: str


class QueryResponse(BaseModel):
    response: str
    sources: Optional[List[str]] = []


class ReminderRequest(BaseModel):
    event_name: str
    event_date: str
    event_time: str
    details: Optional[str] = ""


@app.on_event("startup")
async def startup_event():
    """Initialize all services on startup"""
    global vector_store, agent, calendar_service
    
    print("🚀 Initializing Context-Aware Agent...")
    
    # Initialize vector store
    vector_store = VectorStore()
    vector_store.initialize()
    
    # Initialize calendar service
    calendar_service = CalendarService()
    
    # Initialize agent
    agent = ContextAwareAgent(vector_store, calendar_service)
    
    print("✅ Agent initialized successfully!")


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "running",
        "service": "Context-Aware Personal Executive",
        "version": "1.0.0"
    }


@app.post("/ask", response_model=QueryResponse)
async def ask_question(request: QueryRequest):
    """
    Process user query and return AI-generated response
    
    The agent will automatically decide which tools to use based on the query.
    """
    try:
        if not agent:
            raise HTTPException(status_code=500, detail="Agent not initialized")
        
        print(f"📝 Processing query: {request.query}")
        
        # Get response from agent
        response = agent.process_query(request.query)
        
        return QueryResponse(
            response=response["answer"],
            sources=response.get("sources", [])
        )
        
    except Exception as e:
        print(f"❌ Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/events")
async def get_events():
    """
    Get upcoming calendar events
    """
    try:
        if not calendar_service:
            raise HTTPException(status_code=500, detail="Calendar service not initialized")
        
        events = calendar_service.get_upcoming_events()
        return {"events": events}
        
    except Exception as e:
        print(f"❌ Error fetching events: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/reminder")
async def send_reminder(request: ReminderRequest):
    """
    Send a reminder notification for an event
    """
    try:
        if not calendar_service:
            raise HTTPException(status_code=500, detail="Calendar service not initialized")
        
        reminder = calendar_service.create_reminder(
            event_name=request.event_name,
            event_date=request.event_date,
            event_time=request.event_time,
            details=request.details
        )
        
        return {
            "status": "success",
            "reminder": reminder
        }
        
    except Exception as e:
        print(f"❌ Error sending reminder: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/check-reminders")
async def check_reminders():
    """
    Check for upcoming events that need reminders
    This endpoint is called by n8n workflow
    """
    try:
        if not calendar_service:
            raise HTTPException(status_code=500, detail="Calendar service not initialized")
        
        reminders = calendar_service.check_upcoming_reminders()
        
        return {
            "status": "success",
            "reminders": reminders,
            "count": len(reminders)
        }
        
    except Exception as e:
        print(f"❌ Error checking reminders: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/stats")
async def get_stats():
    """
    Get system statistics
    """
    try:
        doc_count = vector_store.get_document_count() if vector_store else 0
        event_count = len(calendar_service.get_upcoming_events()) if calendar_service else 0
        
        return {
            "documents_indexed": doc_count,
            "upcoming_events": event_count,
            "agent_status": "active" if agent else "inactive"
        }
        
    except Exception as e:
        print(f"❌ Error fetching stats: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
