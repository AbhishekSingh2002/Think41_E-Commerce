import React, { useState } from 'react';
import { useChat } from '../../contexts/ChatContext';
import MessageList from '../MessageList/MessageList';
import UserInput from '../UserInput/UserInput';
import ConversationList from '../ConversationList/ConversationList';
import { FiMenu, FiX } from 'react-icons/fi';
import './ChatWindow.css';

const ChatWindow = () => {
  const { messages, isLoading } = useChat();
  const [showSidebar, setShowSidebar] = useState(window.innerWidth > 768);

  const toggleSidebar = () => {
    setShowSidebar(!showSidebar);
  };

  return (
    <div className="chat-window">
      <div className={`sidebar-overlay ${showSidebar ? 'active' : ''}`} 
           onClick={() => setShowSidebar(false)}></div>
      
      <div className={`conversation-sidebar ${showSidebar ? 'show' : ''}`}>
        <ConversationList />
      </div>
      
      <div className="chat-container">
        <div className="chat-header">
          <button className="menu-button" onClick={toggleSidebar} aria-label="Toggle menu">
            {showSidebar ? <FiX /> : <FiMenu />}
          </button>
          <h2>Chat with AI Assistant</h2>
          {isLoading && <div className="typing-indicator">AI is typing...</div>}
        </div>
        <MessageList messages={messages} isLoading={isLoading} />
        <UserInput />
      </div>
    </div>
  );
};

export default ChatWindow;
