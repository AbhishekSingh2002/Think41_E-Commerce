import React, { createContext, useContext, useReducer } from 'react';

// Action types
const SEND_MESSAGE = 'SEND_MESSAGE';
const SET_LOADING = 'SET_LOADING';
const SET_INPUT_VALUE = 'SET_INPUT_VALUE';
const ADD_MESSAGE = 'ADD_MESSAGE';

// Initial state
const initialState = {
  messages: [
    { id: 1, text: 'Hello! How can I help you today?', sender: 'ai' },
  ],
  isLoading: false,
  inputValue: '',
};

// Reducer function
const chatReducer = (state, action) => {
  switch (action.type) {
    case SEND_MESSAGE:
      return {
        ...state,
        messages: [...state.messages, {
          id: state.messages.length + 1,
          text: state.inputValue,
          sender: 'user',
        }],
        inputValue: '',
        isLoading: true,
      };
    
    case ADD_MESSAGE:
      return {
        ...state,
        messages: [...state.messages, {
          id: state.messages.length + 1,
          text: action.payload,
          sender: 'ai',
        }],
        isLoading: false,
      };
    
    case SET_LOADING:
      return {
        ...state,
        isLoading: action.payload,
      };
    
    case SET_INPUT_VALUE:
      return {
        ...state,
        inputValue: action.payload,
      };
    
    default:
      return state;
  }
};

// Create context
const ChatContext = createContext();

// Provider component
export const ChatProvider = ({ children }) => {
  const [state, dispatch] = useReducer(chatReducer, initialState);

  // Action creators
  const sendMessage = async () => {
    if (!state.inputValue.trim()) return;
    
    const userMessage = state.inputValue;
    
    // Dispatch user message
    dispatch({ type: SEND_MESSAGE });
    
    try {
      // Here you would typically make an API call to your backend
      // For now, we'll simulate a response after a short delay
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Simulate AI response
      const response = `I received your message: "${userMessage}"`;
      dispatch({ type: ADD_MESSAGE, payload: response });
    } catch (error) {
      console.error('Error sending message:', error);
      dispatch({ type: ADD_MESSAGE, payload: 'Sorry, something went wrong. Please try again.' });
    }
  };

  const setInputValue = (value) => {
    dispatch({ type: SET_INPUT_VALUE, payload: value });
  };

  const value = {
    messages: state.messages,
    isLoading: state.isLoading,
    inputValue: state.inputValue,
    sendMessage,
    setInputValue,
  };

  return <ChatContext.Provider value={value}>{children}</ChatContext.Provider>;
};

// Custom hook to use the chat context
export const useChat = () => {
  const context = useContext(ChatContext);
  if (context === undefined) {
    throw new Error('useChat must be used within a ChatProvider');
  }
  return context;
};
