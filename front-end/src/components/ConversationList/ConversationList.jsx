import React from 'react';
import { useChat } from '../../contexts/ChatContext';
import './ConversationList.css';

const ConversationList = () => {
  const { 
    conversations, 
    currentConversationId, 
    loadConversation,
    addNewConversation 
  } = useChat();

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleString('en-US', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const getConversationTitle = (conversation) => {
    if (conversation.title !== 'New Chat') return conversation.title;
    
    const firstUserMessage = conversation.messages.find(m => m.sender === 'user');
    return firstUserMessage?.text?.substring(0, 30) + 
      (firstUserMessage?.text.length > 30 ? '...' : '') || 'New Chat';
  };

  return (
    <div className="conversation-list">
      <div className="conversation-header">
        <h3>Chats</h3>
        <button 
          onClick={addNewConversation}
          className="new-chat-button"
          aria-label="Start new chat"
        >
          + New Chat
        </button>
      </div>
      
      <div className="conversation-items">
        {conversations.map((conversation) => (
          <div
            key={conversation.id}
            className={`conversation-item ${
              conversation.id === currentConversationId ? 'active' : ''
            }`}
            onClick={() => loadConversation(conversation.id)}
          >
            <div className="conversation-title">
              {getConversationTitle(conversation)}
            </div>
            <div className="conversation-date">
              {formatDate(conversation.updatedAt)}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ConversationList;
