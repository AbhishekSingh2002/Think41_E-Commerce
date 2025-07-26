import React from 'react';
import './Message.css';

const Message = ({ text, isUser }) => {
  return (
    <div className={`message ${isUser ? 'user-message' : 'ai-message'}`}>
      <div className="message-content">
        {text}
      </div>
    </div>
  );
};

export default Message;
