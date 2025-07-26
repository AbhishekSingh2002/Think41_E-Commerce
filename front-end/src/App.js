import React from 'react';
import { ChatProvider } from './contexts/ChatContext';
import ChatWindow from './components/ChatWindow/ChatWindow';
import './App.css';

function App() {
  return (
    <ChatProvider>
      <div className="app">
        <ChatWindow />
      </div>
    </ChatProvider>
  );
}

export default App;
