import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// API Service Functions
export const apiService = {
  // Ask a question to the AI agent
  askQuestion: async (query) => {
    try {
      const response = await api.post('/ask', { query });
      return response.data;
    } catch (error) {
      console.error('Error asking question:', error);
      throw error;
    }
  },

  // Get upcoming events
  getEvents: async () => {
    try {
      const response = await api.get('/events');
      return response.data;
    } catch (error) {
      console.error('Error fetching events:', error);
      throw error;
    }
  },

  // Send a reminder
  sendReminder: async (reminderData) => {
    try {
      const response = await api.post('/reminder', reminderData);
      return response.data;
    } catch (error) {
      console.error('Error sending reminder:', error);
      throw error;
    }
  },

  // Check for upcoming reminders
  checkReminders: async () => {
    try {
      const response = await api.get('/check-reminders');
      return response.data;
    } catch (error) {
      console.error('Error checking reminders:', error);
      throw error;
    }
  },

  // Get system stats
  getStats: async () => {
    try {
      const response = await api.get('/stats');
      return response.data;
    } catch (error) {
      console.error('Error fetching stats:', error);
      throw error;
    }
  },

  // Health check
  healthCheck: async () => {
    try {
      const response = await api.get('/');
      return response.data;
    } catch (error) {
      console.error('Error checking health:', error);
      throw error;
    }
  },
};

export default api;
