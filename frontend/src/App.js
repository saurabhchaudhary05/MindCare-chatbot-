import React, { useState } from "react";
import "./App.css";

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [darkMode, setDarkMode] = useState(false);

  const addMessage = (sender, text) => {
    setMessages((prev) => [...prev, { sender, text }]);
  };

  const sendMessage = async () => {
    if (!input.trim()) return;
    addMessage("user", input);
    const userMessage = input;
    setInput("");

    try {
      const res = await fetch("http://127.0.0.1:5000/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMessage }),
      });
      const data = await res.json();
      addMessage("bot", data.reply);

      if (data.intervention) {
        alert(`💡 Suggestion: ${data.intervention_text}`);
      }
    } catch (err) {
      console.error(err);
      addMessage("bot", "Sorry, something went wrong.");
    }
  };

  const endChat = async () => {
    try {
      const res = await fetch("http://127.0.0.1:5000/api/summary");
      const data = await res.json();
      alert(
        `📊 Chat Summary:\nDominant Mood: ${data.dominant_mood}\nAverage Score: ${data.avg_score}\nTip: ${
          data.summary
        }\nGoodbye! 👋`
      );
      setMessages([]);
    } catch (err) {
      console.error(err);
      alert("Could not fetch summary.");
    }
  };

  return (
    <div className={`app-container ${darkMode ? "dark" : "light"}`}>
      <div className="chat-container">
        <div className="header-bar">
          <h2 className="header">MindCare Chatbot</h2>
          <div className="mode-toggle">
            <label>
              <input
                type="checkbox"
                checked={darkMode}
                onChange={() => setDarkMode(!darkMode)}
              />{" "}
              Dark Mode
            </label>
          </div>
        </div>

        <div className="chat-box">
          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`chat-message ${
                msg.sender === "user" ? "user" : "bot"
              }`}
            >
              {msg.text}
            </div>
          ))}
        </div>

        <div className="input-area">
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type a message..."
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                e.preventDefault();
                sendMessage();
              }
            }}
          />
          <button onClick={sendMessage}>Send</button>
          <button onClick={endChat} className="end-chat">
            End Chat
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;
