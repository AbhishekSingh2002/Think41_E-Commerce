import React from 'react';
import { useChat } from '../../contexts/ChatContext';
import './UserInput.css';

const UserInput = () => {
  const { inputValue, setInputValue, sendMessage, isLoading } = useChat();

  const handleSubmit = (e) => {
    e.preventDefault();
    if (inputValue.trim() === '' || isLoading) return;
    sendMessage();
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <form className="user-input" onSubmit={handleSubmit}>
      <div className="input-container">
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Type your message..."
          className="message-input"
          disabled={isLoading}
        />
        <button 
          type="submit" 
          className="send-button"
          disabled={!inputValue.trim() || isLoading}
          aria-label="Send message"
        >
          <svg 
            xmlns="http://www.w3.org/2000/svg" 
            viewBox="0 0 24 24" 
            fill="currentColor" 
            className="send-icon"
          >
            <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z" />
          </svg>
        </button>
      </div>
    </form>
  );
};

export default UserInput;
