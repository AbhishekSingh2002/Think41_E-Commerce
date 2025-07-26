import React from 'react';
import { useChat } from '../../contexts/ChatContext';
import MessageList from '../MessageList/MessageList';
import UserInput from '../UserInput/UserInput';
import './ChatWindow.css';

const ChatWindow = () => {
  const { messages, isLoading } = useChat();

  return (
    <div className="chat-window">
      <div className="chat-header">
        <h2>Chat with AI Assistant</h2>
        {isLoading && <div className="typing-indicator">AI is typing...</div>}
      </div>
      <MessageList messages={messages} isLoading={isLoading} />
      <UserInput />
    </div>
  );
};

export default ChatWindow;
