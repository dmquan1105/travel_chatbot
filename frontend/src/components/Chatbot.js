import React, { useState } from 'react';

const Chatbot = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMsg = { sender: 'user', text: input };
    setMessages(prev => [...prev, userMsg]);

    try {
      const response = await fetch("http://localhost:5000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: input })
      });

      if (!response.ok) {
        throw new Error(`Lỗi server: ${response.status}`);
      }

      const data = await response.json();
      const botMsg = { sender: 'bot', text: data.reply };
      setMessages(prev => [...prev, botMsg]);
    } catch (error) {
      setMessages(prev => [
        ...prev,
        { sender: 'bot', text: `Lỗi khi gửi tin nhắn: ${error.message}` }
      ]);
    }

    setInput("");
  };

  return (
    <div style={{ padding: '20px' }}>
      <div style={{
        height: '300px',
        overflowY: 'scroll',
        border: '1px solid #ccc',
        padding: '10px',
        marginBottom: '10px'
      }}>
        {messages.map((msg, index) => (
          <div key={index} style={{ textAlign: msg.sender === 'user' ? 'right' : 'left' }}>
            <p><strong>{msg.sender === 'user' ? 'Bạn' : 'Bot'}:</strong> {msg.text}</p>
          </div>
        ))}
      </div>
      <div style={{ display: 'flex' }}>
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && handleSend()}
          style={{ flex: 1, padding: '8px' }}
          placeholder="Nhập câu hỏi..."
        />
        <button onClick={handleSend} style={{ padding: '8px 16px' }}>Gửi</button>
      </div>
    </div>
  );
};

export default Chatbot;
