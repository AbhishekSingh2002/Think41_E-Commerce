import React from 'react';
import { useChat } from '../../contexts/ChatContext';
import Message from '../Message/Message';
import './MessageList.css';

const MessageList = () => {
  const { messages, isLoading } = useChat();
  const messagesEndRef = React.useRef(null);

  // Auto-scroll to bottom when messages change
  React.useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div className="message-list">
      {messages.map((message) => (
        <Message 
          key={message.id}
          text={message.text}
          isUser={message.sender === 'user'}
        />
      ))}
      {isLoading && (
        <div className="typing-bubble">
          <div className="typing-dot"></div>
          <div className="typing-dot"></div>
          <div className="typing-dot"></div>
        </div>
      )}
      <div ref={messagesEndRef} />
    </div>
  );
};

export default MessageList;
