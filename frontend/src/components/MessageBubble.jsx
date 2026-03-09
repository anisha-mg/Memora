import React from 'react';

const MessageBubble = ({ message }) => {
  const isUser = message.sender === 'user';

  const formatTime = (timestamp) => {
    const date = new Date(timestamp);
    return date.toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div
        className={`max-w-[78%] rounded-2xl px-4 py-2.5 shadow-sm ${
          isUser
            ? 'bg-blue-600 text-white rounded-br-md'
            : 'bg-white text-slate-800 border border-slate-200 rounded-bl-md'
        }`}
      >
        <div className="break-words whitespace-pre-wrap">{message.text}</div>
        
        {/* Display sources if available */}
        {message.sources && message.sources.length > 0 && (
          <div className="mt-2 border-t border-slate-200 pt-2">
            <div className="text-xs opacity-75">
              Sources: {message.sources.join(', ')}
            </div>
          </div>
        )}
        
        <div
          className={`text-xs mt-1 ${
            isUser ? 'text-blue-100' : 'text-slate-500'
          }`}
        >
          {formatTime(message.timestamp)}
        </div>
      </div>
    </div>
  );
};

export default MessageBubble;
