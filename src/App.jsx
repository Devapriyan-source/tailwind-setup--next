import { useState, useEffect, useRef } from "react";
import { motion } from "framer-motion";
import { Send, Loader, Plus, Menu } from "lucide-react";

const ChatMessage = ({ text, sender }) => (
  <motion.div
    initial={{ opacity: 0, y: 10 }}
    animate={{ opacity: 1, y: 0 }}
    className={`max-w-[80%] px-4 py-2 rounded-lg text-white text-sm shadow-md ${
      sender === "user" ? "bg-blue-500 ml-auto" : "bg-gray-700"
    }`}
  >
    {text}
  </motion.div>
);

const Sidebar = ({ chats, onSelectChat, onNewChat }) => (
  <div className="w-64 bg-white/10 backdrop-blur-md p-4 border-r border-white/20 hidden md:flex flex-col">
    <button
      onClick={onNewChat}
      className="flex items-center justify-center w-full p-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
    >
      <Plus className="mr-2" /> New Chat
    </button>
    <div className="mt-4 flex-1 overflow-y-auto">
      {chats.map((chat, index) => (
        <button
          key={index}
          onClick={() => onSelectChat(chat)}
          className="block w-full p-2 text-white bg-white/10 hover:bg-white/20 rounded-md mb-2"
        >
          {chat.title}
        </button>
      ))}
    </div>
  </div>
);

export default function MentauraChat() {
  const [messages, setMessages] = useState([
    { text: "Hello! I'm Mentaura. How can I support you today?", sender: "bot" }
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [chats, setChats] = useState([]);
  const chatRef = useRef(null);

  useEffect(() => {
    chatRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim()) return;
    
    setMessages([...messages, { text: input, sender: "user" }]);
    setInput("");
    setLoading(true);
  
    try {
      const response = await fetch("http://127.0.0.1:8000/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query: input }), // Fix: Use "query" to match FastAPI model
      });
  
      if (!response.ok) {
        throw new Error("Server error");
      }
  
      const data = await response.json();
      setMessages((prev) => [...prev, { text: data.response, sender: "bot" }]);
    } catch (error) {
      console.error("Error:", error);
    } finally {
      setLoading(false);
    }
  };
  
  

  const handleNewChat = () => {
    setChats([...chats, { title: `Chat ${chats.length + 1}`, messages: [] }]);
    setMessages([{ text: "Hello! I'm Mentaura. How can I support you today?", sender: "bot" }]);
  };

  return (
    <div className="flex h-screen w-full bg-gradient-to-br from-blue-800 to-purple-900">
      <Sidebar chats={chats} onSelectChat={() => {}} onNewChat={handleNewChat} />
      
      <div className="flex flex-col flex-1 items-center p-4">
        <h2 className="text-white text-2xl font-bold text-center mb-4">Mentaura</h2>
        
        <div className="flex-1 w-full max-w-2xl overflow-y-auto p-4 space-y-3 scrollbar-hide bg-white/10 rounded-lg">
          {messages.map((msg, index) => (
            <ChatMessage key={index} text={msg.text} sender={msg.sender} />
          ))}
          <div ref={chatRef}></div>
        </div>
        
        <div className="flex items-center w-full max-w-2xl mt-4 bg-white/20 rounded-full p-2">
          <input
            type="text"
            className="flex-1 bg-transparent text-white outline-none px-3"
            placeholder="Type a message..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
          />
          <button onClick={sendMessage} className="text-white p-2 hover:scale-110 transition-all">
            {loading ? <Loader className="animate-spin" /> : <Send />}
          </button>
        </div>
      </div>
    </div>
  );
}




