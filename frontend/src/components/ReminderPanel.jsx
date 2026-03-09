import React, { useState, useEffect } from 'react';
import { CalendarIcon, ClockIcon, BellIcon } from '@heroicons/react/24/outline';

const ReminderPanel = () => {
  const [events, setEvents] = useState([]);
  const [reminders, setReminders] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchEvents();
    fetchReminders();

    // Poll for new reminders every 5 minutes
    const interval = setInterval(() => {
      fetchReminders();
    }, 5 * 60 * 1000);

    return () => clearInterval(interval);
  }, []);

  const fetchEvents = async () => {
    try {
      const response = await fetch('http://localhost:8000/events');
      const data = await response.json();
      setEvents(data.events || []);
    } catch (error) {
      console.error('Error fetching events:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchReminders = async () => {
    try {
      const response = await fetch('http://localhost:8000/check-reminders');
      const data = await response.json();
      setReminders(data.reminders || []);
    } catch (error) {
      console.error('Error fetching reminders:', error);
    }
  };

  const getDaysUntilText = (daysUntil) => {
    if (daysUntil === 0) return 'Today';
    if (daysUntil === 1) return 'Tomorrow';
    return `In ${daysUntil} days`;
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-full space-y-4">
      {/* Active Reminders */}
      {reminders.length > 0 && (
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
          <div className="flex items-center mb-3">
            <BellIcon className="h-5 w-5 text-yellow-600 mr-2" />
            <h3 className="text-lg font-semibold text-yellow-800">
              Active Reminders
            </h3>
          </div>
          <div className="space-y-2">
            {reminders.map((reminder, index) => (
              <div
                key={index}
                className="bg-white p-3 rounded border border-yellow-300"
              >
                <div className="font-medium text-gray-800">
                  {reminder.event}
                </div>
                <div className="text-sm text-gray-600 mt-1">
                  {reminder.date} at {reminder.time}
                </div>
                <div className="text-xs text-yellow-700 mt-1">
                  ⏰ In {reminder.hours_until} hours
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Upcoming Events */}
      <div className="bg-white rounded-lg shadow-lg p-4 flex-1 overflow-y-auto">
        <div className="flex items-center mb-4">
          <CalendarIcon className="h-5 w-5 text-blue-600 mr-2" />
          <h3 className="text-lg font-semibold text-gray-800">
            Upcoming Events
          </h3>
        </div>

        {events.length === 0 ? (
          <div className="text-center text-gray-500 py-8">
            No upcoming events
          </div>
        ) : (
          <div className="space-y-3">
            {events.map((event, index) => (
              <div
                key={index}
                className="border border-gray-200 rounded-lg p-3 hover:shadow-md transition-shadow"
              >
                <div className="font-medium text-gray-800">{event.event}</div>
                <div className="flex items-center mt-2 text-sm text-gray-600">
                  <CalendarIcon className="h-4 w-4 mr-1" />
                  <span>{event.date}</span>
                </div>
                <div className="flex items-center mt-1 text-sm text-gray-600">
                  <ClockIcon className="h-4 w-4 mr-1" />
                  <span>{event.time}</span>
                </div>
                <div className="mt-2">
                  <span
                    className={`inline-block px-2 py-1 text-xs rounded-full ${
                      event.days_until === 0
                        ? 'bg-red-100 text-red-800'
                        : event.days_until === 1
                        ? 'bg-yellow-100 text-yellow-800'
                        : 'bg-blue-100 text-blue-800'
                    }`}
                  >
                    {getDaysUntilText(event.days_until)}
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Stats Footer */}
      <div className="bg-gray-50 rounded-lg p-3 text-sm text-gray-600">
        <div className="flex justify-between">
          <span>Total Events:</span>
          <span className="font-semibold">{events.length}</span>
        </div>
        <div className="flex justify-between mt-1">
          <span>Active Reminders:</span>
          <span className="font-semibold text-yellow-600">
            {reminders.length}
          </span>
        </div>
      </div>
    </div>
  );
};

export default ReminderPanel;
