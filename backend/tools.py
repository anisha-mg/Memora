"""
Data Access Tools for the Context-Aware Agent
"""
import os
import pandas as pd
import PyPDF2
from typing import List, Dict, Optional
from datetime import datetime, timedelta


class DataTools:
    """Collection of tools for accessing different data sources"""
    
    def __init__(self, data_dir: str = "./data"):
        self.data_dir = data_dir
        self.emails_path = os.path.join(data_dir, "emails.txt")
        self.events_path = os.path.join(data_dir, "events.csv")
        self.pdf_path = os.path.join(data_dir, "notes.pdf")
        
    def search_email(self, query: str) -> str:
        """
        Search through email data for relevant information
        
        Args:
            query: Search query
            
        Returns:
            Relevant email content
        """
        try:
            if not os.path.exists(self.emails_path):
                return "No email data found."
            
            with open(self.emails_path, 'r', encoding='utf-8') as f:
                email_content = f.read()
            
            # Simple keyword matching (in production, use better search)
            query_lower = query.lower()
            lines = email_content.split('\n')
            relevant_lines = []
            
            for i, line in enumerate(lines):
                if any(keyword in line.lower() for keyword in query_lower.split()):
                    # Include context: previous and next lines
                    start = max(0, i - 2)
                    end = min(len(lines), i + 3)
                    relevant_lines.extend(lines[start:end])
            
            if relevant_lines:
                result = '\n'.join(list(dict.fromkeys(relevant_lines)))  # Remove duplicates
                return f"Found in emails:\n{result}"
            else:
                return f"No relevant email found for query: {query}"
                
        except Exception as e:
            return f"Error searching emails: {str(e)}"
    
    def search_pdf(self, query: str) -> str:
        """
        Search through PDF documents for relevant information
        
        Args:
            query: Search query
            
        Returns:
            Relevant PDF content
        """
        try:
            if not os.path.exists(self.pdf_path):
                return "No PDF documents found."
            
            # Read PDF content
            with open(self.pdf_path, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                text_content = []
                
                for page in pdf_reader.pages:
                    text_content.append(page.extract_text())
                
                full_text = '\n'.join(text_content)
            
            # Simple keyword search
            query_lower = query.lower()
            paragraphs = full_text.split('\n\n')
            relevant_paragraphs = []
            
            for para in paragraphs:
                if any(keyword in para.lower() for keyword in query_lower.split()):
                    relevant_paragraphs.append(para.strip())
            
            if relevant_paragraphs:
                result = '\n\n'.join(relevant_paragraphs[:3])  # Limit to top 3 paragraphs
                return f"Found in PDF documents:\n{result}"
            else:
                return f"No relevant PDF content found for query: {query}"
                
        except Exception as e:
            return f"Error searching PDFs: {str(e)}"
    
    def search_csv(self, query: str) -> str:
        """
        Search through CSV files for relevant information
        
        Args:
            query: Search query
            
        Returns:
            Relevant CSV data
        """
        try:
            if not os.path.exists(self.events_path):
                return "No CSV data found."
            
            # Read CSV
            df = pd.read_csv(self.events_path)
            
            # Search across all columns
            query_lower = query.lower()
            mask = df.apply(lambda row: row.astype(str).str.contains(query_lower, case=False).any(), axis=1)
            filtered_df = df[mask]
            
            if not filtered_df.empty:
                result = filtered_df.to_string(index=False)
                return f"Found in CSV data:\n{result}"
            else:
                return f"No relevant CSV data found for query: {query}"
                
        except Exception as e:
            return f"Error searching CSV: {str(e)}"
    
    def get_calendar_events(self, days_ahead: int = 7) -> str:
        """
        Get calendar events for the next N days
        
        Args:
            days_ahead: Number of days to look ahead
            
        Returns:
            Formatted list of upcoming events
        """
        try:
            if not os.path.exists(self.events_path):
                return "No calendar events found."
            
            df = pd.read_csv(self.events_path)
            
            # Parse dates
            df['date'] = pd.to_datetime(df['date'])
            today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            cutoff = today + timedelta(days=days_ahead)
            
            # Filter upcoming events
            upcoming = df[(df['date'] >= today) & (df['date'] <= cutoff)]
            upcoming = upcoming.sort_values('date')
            
            if not upcoming.empty:
                events_list = []
                for _, row in upcoming.iterrows():
                    event_str = f"• {row['event']} on {row['date'].strftime('%Y-%m-%d')} at {row['time']}"
                    events_list.append(event_str)
                
                return "Upcoming events:\n" + "\n".join(events_list)
            else:
                return f"No events scheduled in the next {days_ahead} days."
                
        except Exception as e:
            return f"Error fetching calendar events: {str(e)}"
    
    def send_reminder(self, event_name: str, event_date: str, event_time: str, details: str = "") -> str:
        """
        Create a reminder notification
        
        Args:
            event_name: Name of the event
            event_date: Date of the event
            event_time: Time of the event
            details: Additional event details
            
        Returns:
            Formatted reminder message
        """
        try:
            reminder_msg = f"📅 REMINDER: {event_name}\n"
            reminder_msg += f"📆 Date: {event_date}\n"
            reminder_msg += f"⏰ Time: {event_time}\n"
            
            if details:
                reminder_msg += f"📝 Details: {details}\n"
            
            return reminder_msg
            
        except Exception as e:
            return f"Error creating reminder: {str(e)}"


# Tool definitions for LangChain agent
def get_tool_definitions():
    """
    Return tool definitions for the LangChain agent
    """
    return [
        {
            "name": "search_email",
            "description": "Search through email data for relevant information. Use this when the user asks about emails, messages, or communications.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query to find relevant emails"
                    }
                },
                "required": ["query"]
            }
        },
        {
            "name": "search_pdf",
            "description": "Search through PDF documents for relevant information. Use this when the user asks about documents, notes, or written content.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query to find relevant PDF content"
                    }
                },
                "required": ["query"]
            }
        },
        {
            "name": "search_csv",
            "description": "Search through CSV data files for structured information. Use this when the user asks about data, tables, or structured records.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query to find relevant CSV data"
                    }
                },
                "required": ["query"]
            }
        },
        {
            "name": "get_calendar_events",
            "description": "Get upcoming calendar events. Use this when the user asks about schedule, meetings, events, or what's coming up.",
            "parameters": {
                "type": "object",
                "properties": {
                    "days_ahead": {
                        "type": "integer",
                        "description": "Number of days to look ahead (default: 7)",
                        "default": 7
                    }
                },
                "required": []
            }
        },
        {
            "name": "send_reminder",
            "description": "Create a reminder notification for an event. Use this when explicitly asked to send or create a reminder.",
            "parameters": {
                "type": "object",
                "properties": {
                    "event_name": {
                        "type": "string",
                        "description": "Name of the event"
                    },
                    "event_date": {
                        "type": "string",
                        "description": "Date of the event (YYYY-MM-DD format)"
                    },
                    "event_time": {
                        "type": "string",
                        "description": "Time of the event (HH:MM format)"
                    },
                    "details": {
                        "type": "string",
                        "description": "Additional event details",
                        "default": ""
                    }
                },
                "required": ["event_name", "event_date", "event_time"]
            }
        }
    ]
