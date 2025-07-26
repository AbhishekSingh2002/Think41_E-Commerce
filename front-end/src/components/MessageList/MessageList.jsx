import React from 'react';
import Message from '../Message/Message';
import './MessageList.css';

const MessageList = ({ messages }) => {
  return (
    <div className="message-list">
      {messages.map((message) => (
        <Message 
          key={message.id}
          text={message.text}
          isUser={message.sender === 'user'}
        />
      ))}
    </div>
  );
};

export default MessageList;
