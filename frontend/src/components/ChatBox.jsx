import React, { useState } from 'react';
import MessageBubble from './MessageBubble';

const ChatBox = ({ onFetchUpdate }) => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      text: "Hello! I'm your personal executive assistant. I can help you find information from your emails, documents, and calendar. What would you like to know?",
      sender: 'ai',
      timestamp: new Date().toISOString(),
    },
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const quickActions = [
    'Show my next calendar event',
    'Summarize latest email updates',
    'Create a reminder for tomorrow',
  ];

  const handleSend = async (overrideText) => {
    const messageText = (overrideText ?? inputValue).trim();
    if (!messageText) return;

    const userMessage = {
      id: Date.now(),
      text: messageText,
      sender: 'user',
      timestamp: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);
    onFetchUpdate?.({ isLoading: true });

    try {
      const response = await fetch('http://localhost:8000/ask', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: messageText }),
      });

      const data = await response.json();

      const aiMessage = {
        id: Date.now() + 1,
        text: data.response,
        sender: 'ai',
        timestamp: new Date().toISOString(),
        sources: data.sources || [],
      };

      setMessages((prev) => [...prev, aiMessage]);
      onFetchUpdate?.({
        isLoading: false,
        completed: true,
        query: messageText,
        sources: data.sources || [],
        timestamp: new Date().toISOString(),
      });
    } catch (error) {
      console.error('Error:', error);
      const errorMessage = {
        id: Date.now() + 1,
        text: 'Sorry, I encountered an error. Please make sure the backend server is running.',
        sender: 'ai',
        timestamp: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, errorMessage]);
      onFetchUpdate?.({
        isLoading: false,
        completed: true,
        query: messageText,
        sources: [],
        error: true,
        timestamp: new Date().toISOString(),
      });
    } finally {
      setIsLoading(false);
      onFetchUpdate?.({ isLoading: false });
    }
  };

  const runQuickAction = (prompt) => {
    if (isLoading) return;
    handleSend(prompt);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="flex h-full flex-col overflow-hidden rounded-3xl bg-white shadow-xl">
      <div className="bg-gradient-to-r from-slate-900 via-slate-800 to-slate-900 px-5 py-3 text-white">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="flex h-8 w-8 items-center justify-center rounded-full bg-blue-500 text-sm font-bold">
              M
            </div>
            <div>
              <h2 className="text-sm font-semibold">Memora Bot</h2>
              <p className="text-xs text-slate-300">AI Assistant</p>
            </div>
          </div>
          <div className="h-8 w-8 rounded-full border border-slate-600" />
        </div>
      </div>

      <div className="flex-1 space-y-4 overflow-y-auto bg-slate-50 px-4 py-4">
        {messages.map((message) => (
          <MessageBubble key={message.id} message={message} />
        ))}

        <div className="space-y-2">
          {quickActions.map((action) => (
            <button
              key={action}
              type="button"
              onClick={() => runQuickAction(action)}
              className="block rounded-full border border-slate-300 bg-white px-3 py-1.5 text-left text-xs text-slate-700 transition hover:border-blue-400 hover:text-blue-700"
            >
              {action}
            </button>
          ))}
        </div>

        {isLoading && (
          <div className="flex items-center space-x-2 text-slate-500">
            <div className="animate-pulse">●</div>
            <div className="animate-pulse animation-delay-200">●</div>
            <div className="animate-pulse animation-delay-400">●</div>
            <span className="ml-2">Thinking...</span>
          </div>
        )}
      </div>

      <div className="border-t border-slate-200 bg-white p-3">
        <div className="flex items-center gap-2 rounded-full border border-slate-200 px-3 py-2">
          <span className="text-slate-400">+</span>
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Write your message..."
            className="flex-1 bg-transparent text-sm text-slate-700 outline-none"
            disabled={isLoading}
          />
          <button
            onClick={handleSend}
            disabled={isLoading || !inputValue.trim()}
            className="rounded-full bg-blue-600 px-4 py-1.5 text-sm text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:bg-slate-300"
          >
            Send
          </button>
        </div>
        <div className="mt-2 text-center text-[11px] text-slate-400">
          Try: "What did we decide about logistics?" or "When is the next meeting?"
        </div>
      </div>
    </div>
  );
};

export default ChatBox;
