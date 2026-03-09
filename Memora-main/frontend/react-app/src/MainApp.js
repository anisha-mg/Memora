import { useState } from "react";
import ChatMessage from "./components/ChatMessage";
import ChatInput from "./components/ChatInput";
import Sidebar from "./components/Sidebar";

function App() {

  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const sendMessage = (text) => {

    const userMessage = {
      sender: "user",
      text: text
    };

    setMessages((prev) => [...prev, userMessage]);
    setLoading(true);

    setTimeout(() => {

      const agentMessage = {
        sender: "agent",
        text: "The logistics were finalized in Monday's email thread.",
        source: "Email",
        tool: "search_email"
      };

      setMessages((prev) => [...prev, agentMessage]);
      setLoading(false);

    }, 1500);
  };

  return (

    <div className="flex h-screen">

      <Sidebar />

      <div className="flex flex-col flex-1">

        <header className="p-4 border-b font-bold">
          Context-Aware Personal Executive
        </header>

        <div className="flex-1 overflow-y-auto p-6 bg-gray-100">

          {messages.map((msg, index) => (
            <ChatMessage key={index} message={msg} />
          ))}

          {loading && (
            <div className="text-gray-500">
              Agent is thinking...
            </div>
          )}

        </div>

        <ChatInput onSend={sendMessage} />

      </div>

    </div>

  );
}

export default App;
