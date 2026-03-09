function ChatMessage({ message }) {
  const isUser = message.sender === "user";

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"} mb-4`}>
      <div
        className={`p-3 rounded-xl max-w-lg ${
          isUser
            ? "bg-blue-500 text-white"
            : "bg-gray-200 text-black"
        }`}
      >
        <p>{message.text}</p>

        {message.source && (
          <div className="text-sm mt-2">
            Source: <b>{message.source}</b>
          </div>
        )}

        {message.tool && (
          <div className="text-xs text-gray-600">
            Tool Used: {message.tool}
          </div>
        )}
      </div>
    </div>
  );
}

export default ChatMessage;