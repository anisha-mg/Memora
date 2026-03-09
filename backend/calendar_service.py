"""
Calendar Service for managing events and reminders
"""
import os
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict


class CalendarService:
    """
    Service for managing calendar events and automated reminders
    """
    
    def __init__(self, data_dir: str = "./data"):
        """
        Initialize calendar service
        
        Args:
            data_dir: Directory containing calendar data
        """
        self.data_dir = data_dir
        self.events_path = os.path.join(data_dir, "events.csv")
        self.events_df = None
        self._load_events()
    
    def _load_events(self):
        """Load events from CSV file"""
        try:
            if os.path.exists(self.events_path):
                self.events_df = pd.read_csv(self.events_path)
                self.events_df['date'] = pd.to_datetime(self.events_df['date'])
                print(f"✅ Loaded {len(self.events_df)} events from calendar")
            else:
                print("⚠️  No calendar events file found")
                self.events_df = pd.DataFrame(columns=['event', 'date', 'time'])
        except Exception as e:
            print(f"⚠️  Error loading calendar events: {str(e)}")
            self.events_df = pd.DataFrame(columns=['event', 'date', 'time'])
    
    def get_upcoming_events(self, days_ahead: int = 7) -> List[Dict]:
        """
        Get upcoming events within the next N days
        
        Args:
            days_ahead: Number of days to look ahead
            
        Returns:
            List of upcoming events
        """
        if self.events_df is None or self.events_df.empty:
            return []
        
        try:
            today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            cutoff = today + timedelta(days=days_ahead)
            
            # Filter upcoming events
            upcoming = self.events_df[
                (self.events_df['date'] >= today) & 
                (self.events_df['date'] <= cutoff)
            ].copy()
            
            upcoming = upcoming.sort_values('date')
            
            # Convert to list of dictionaries
            events = []
            for _, row in upcoming.iterrows():
                events.append({
                    "event": row['event'],
                    "date": row['date'].strftime('%Y-%m-%d'),
                    "time": row['time'],
                    "days_until": (row['date'] - today).days
                })
            
            return events
            
        except Exception as e:
            print(f"⚠️  Error getting upcoming events: {str(e)}")
            return []
    
    def check_upcoming_reminders(self, hours_ahead: int = 24) -> List[Dict]:
        """
        Check for events that need reminders (within next N hours)
        This is called by the n8n workflow
        
        Args:
            hours_ahead: Number of hours to look ahead (default: 24)
            
        Returns:
            List of events needing reminders
        """
        if self.events_df is None or self.events_df.empty:
            return []
        
        try:
            now = datetime.now()
            cutoff = now + timedelta(hours=hours_ahead)
            
            # Create datetime from date and time
            reminders = []
            
            for _, row in self.events_df.iterrows():
                try:
                    # Parse event datetime
                    event_datetime_str = f"{row['date'].strftime('%Y-%m-%d')} {row['time']}"
                    event_datetime = datetime.strptime(event_datetime_str, '%Y-%m-%d %H:%M')
                    
                    # Check if event is within reminder window
                    if now <= event_datetime <= cutoff:
                        hours_until = (event_datetime - now).total_seconds() / 3600
                        
                        reminders.append({
                            "event": row['event'],
                            "date": row['date'].strftime('%Y-%m-%d'),
                            "time": row['time'],
                            "datetime": event_datetime.isoformat(),
                            "hours_until": round(hours_until, 1),
                            "message": self._format_reminder_message(
                                row['event'],
                                row['date'].strftime('%Y-%m-%d'),
                                row['time'],
                                hours_until
                            )
                        })
                except Exception as e:
                    print(f"⚠️  Error processing event: {str(e)}")
                    continue
            
            return reminders
            
        except Exception as e:
            print(f"⚠️  Error checking reminders: {str(e)}")
            return []
    
    def _format_reminder_message(self, event_name: str, event_date: str, event_time: str, hours_until: float) -> str:
        """
        Format a reminder message
        
        Args:
            event_name: Name of the event
            event_date: Date of the event
            event_time: Time of the event
            hours_until: Hours until the event
            
        Returns:
            Formatted reminder message
        """
        if hours_until < 1:
            time_desc = "in less than an hour"
        elif hours_until < 2:
            time_desc = "in about 1 hour"
        elif hours_until < 24:
            time_desc = f"in about {int(hours_until)} hours"
        else:
            time_desc = "tomorrow"
        
        message = f"📅 REMINDER: {event_name}\n"
        message += f"⏰ {time_desc} at {event_time}\n"
        message += f"📆 {event_date}"
        
        return message
    
    def create_reminder(self, event_name: str, event_date: str, event_time: str, details: str = "") -> Dict:
        """
        Create a reminder for an event
        
        Args:
            event_name: Name of the event
            event_date: Date of the event
            event_time: Time of the event
            details: Additional details
            
        Returns:
            Reminder information
        """
        try:
            # Calculate time until event
            event_datetime_str = f"{event_date} {event_time}"
            event_datetime = datetime.strptime(event_datetime_str, '%Y-%m-%d %H:%M')
            now = datetime.now()
            hours_until = (event_datetime - now).total_seconds() / 3600
            
            message = self._format_reminder_message(event_name, event_date, event_time, hours_until)
            
            if details:
                message += f"\n📝 Details: {details}"
            
            return {
                "event": event_name,
                "date": event_date,
                "time": event_time,
                "message": message,
                "created_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"⚠️  Error creating reminder: {str(e)}")
            return {
                "event": event_name,
                "error": str(e)
            }
    
    def add_event(self, event_name: str, event_date: str, event_time: str):
        """
        Add a new event to the calendar
        
        Args:
            event_name: Name of the event
            event_date: Date of the event (YYYY-MM-DD)
            event_time: Time of the event (HH:MM)
        """
        try:
            new_event = pd.DataFrame([{
                'event': event_name,
                'date': pd.to_datetime(event_date),
                'time': event_time
            }])
            
            self.events_df = pd.concat([self.events_df, new_event], ignore_index=True)
            
            # Save to CSV
            self.events_df.to_csv(self.events_path, index=False)
            
            print(f"✅ Added event: {event_name}")
            
        except Exception as e:
            print(f"⚠️  Error adding event: {str(e)}")
    
    def get_event_by_name(self, event_name: str) -> Dict:
        """
        Get event details by name
        
        Args:
            event_name: Name of the event
            
        Returns:
            Event details or None
        """
        if self.events_df is None or self.events_df.empty:
            return None
        
        try:
            match = self.events_df[
                self.events_df['event'].str.contains(event_name, case=False, na=False)
            ]
            
            if not match.empty:
                row = match.iloc[0]
                return {
                    "event": row['event'],
                    "date": row['date'].strftime('%Y-%m-%d'),
                    "time": row['time']
                }
            
            return None
            
        except Exception as e:
            print(f"⚠️  Error getting event: {str(e)}")
            return None
