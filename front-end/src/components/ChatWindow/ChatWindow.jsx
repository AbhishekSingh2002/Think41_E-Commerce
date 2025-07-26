import React, { useState } from 'react';
import MessageList from '../MessageList/MessageList';
import UserInput from '../UserInput/UserInput';
import './ChatWindow.css';

const ChatWindow = () => {
  const [messages, setMessages] = useState([
    { id: 1, text: 'Hello! How can I help you today?', sender: 'ai' },
  ]);

  const handleSendMessage = (message) => {
    const newMessage = {
      id: messages.length + 1,
      text: message,
      sender: 'user',
    };
    setMessages([...messages, newMessage]);
    
    // Here you would typically send the message to your backend
    // and receive a response to update the messages state
  };

  return (
    <div className="chat-window">
      <div className="chat-header">
        <h2>Chat with AI Assistant</h2>
      </div>
      <MessageList messages={messages} />
      <UserInput onSendMessage={handleSendMessage} />
    </div>
  );
};

export default ChatWindow;
