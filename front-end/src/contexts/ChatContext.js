import React, { createContext, useReducer, useEffect, useContext } from 'react';

// Action types
const SEND_MESSAGE = 'SEND_MESSAGE';
const SET_LOADING = 'SET_LOADING';
const SET_INPUT_VALUE = 'SET_INPUT_VALUE';
const ADD_MESSAGE = 'ADD_MESSAGE';
const ADD_CONVERSATION = 'ADD_CONVERSATION';
const SET_CURRENT_CONVERSATION = 'SET_CURRENT_CONVERSATION';
const LOAD_CONVERSATION = 'LOAD_CONVERSATION';

// Load saved conversations from localStorage or use default
const loadFromLocalStorage = () => {
  try {
    const saved = localStorage.getItem('chat-conversations');
    if (saved) {
      return JSON.parse(saved);
    }
  } catch (error) {
    console.error('Failed to load conversations from localStorage', error);
  }
  
  // Default state if nothing is saved
  return [
    {
      id: 'default',
      title: 'New Chat',
      messages: [
        { id: Date.now(), text: 'Hello! How can I help you today?', sender: 'ai' },
      ],
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    }
  ];
};

// Initial state
const initialState = {
  conversations: loadFromLocalStorage(),
  currentConversationId: loadFromLocalStorage()[0]?.id || 'default',
  isLoading: false,
  inputValue: '',
};

// Helper functions
const updateConversation = (conversations, id, updates) => {
  return conversations.map(conv => 
    conv.id === id ? { ...conv, ...updates, updatedAt: new Date().toISOString() } : conv
  );
};

// Reducer function
const chatReducer = (state, action) => {
  switch (action.type) {
    case SEND_MESSAGE: {
      const newMessage = {
        id: Date.now(),
        text: state.inputValue,
        sender: 'user',
      };
      
      const currentConv = state.conversations.find(c => c.id === state.currentConversationId);
      const isNewConversation = currentConv.messages.length <= 1; // Only has the initial AI message
      
      return {
        ...state,
        conversations: updateConversation(
          state.conversations,
          state.currentConversationId,
          {
            messages: [
              ...currentConv.messages,
              newMessage
            ],
            // If this is a new conversation, use the first message as the title
            ...(isNewConversation && state.inputValue.trim() && {
              title: state.inputValue.trim().substring(0, 50) + (state.inputValue.length > 50 ? '...' : '')
            })
          }
        ),
        inputValue: '',
        isLoading: true,
      };
    }
    
    case ADD_MESSAGE: {
      const newMessage = {
        id: Date.now(),
        text: action.payload,
        sender: 'ai',
      };
      
      return {
        ...state,
        conversations: updateConversation(
          state.conversations,
          state.currentConversationId,
          {
            messages: [
              ...state.conversations.find(c => c.id === state.currentConversationId).messages,
              newMessage
            ]
          }
        ),
        isLoading: false,
      };
    }
    
    case ADD_CONVERSATION: {
      const newConversation = {
        id: `conv-${Date.now()}`,
        title: 'New Chat',
        messages: [
          { id: 1, text: 'Hello! How can I help you today?', sender: 'ai' },
        ],
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
      };
      
      return {
        ...state,
        conversations: [newConversation, ...state.conversations],
        currentConversationId: newConversation.id,
      };
    }
    
    case SET_CURRENT_CONVERSATION:
      return {
        ...state,
        currentConversationId: action.payload,
      };
    
    case LOAD_CONVERSATION: {
      const { conversationId } = action.payload;
      const conversation = state.conversations.find(c => c.id === conversationId);
      
      if (!conversation) return state;
      
      return {
        ...state,
        currentConversationId: conversationId,
      };
    }
    
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

// Save conversations to localStorage whenever they change
const saveToLocalStorage = (conversations) => {
  try {
    localStorage.setItem('chat-conversations', JSON.stringify(conversations));
  } catch (error) {
    console.error('Failed to save conversations to localStorage', error);
  }
};

// Provider component
export const ChatProvider = ({ children }) => {
  const [state, dispatch] = useReducer(chatReducer, initialState);
  
  // Save conversations to localStorage whenever they change
  useEffect(() => {
    saveToLocalStorage(state.conversations);
  }, [state.conversations]);

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
  
  const addNewConversation = () => {
    dispatch({ type: ADD_CONVERSATION });
  };
  
  const loadConversation = (conversationId) => {
    if (conversationId === state.currentConversationId) return;
    dispatch({ type: LOAD_CONVERSATION, payload: { conversationId } });
  };

  const setInputValue = (value) => {
    dispatch({ type: SET_INPUT_VALUE, payload: value });
  };

  const currentConversation = state.conversations.find(
    conv => conv.id === state.currentConversationId
  ) || state.conversations[0];

  const value = {
    messages: currentConversation?.messages || [],
    conversations: state.conversations,
    currentConversationId: state.currentConversationId,
    isLoading: state.isLoading,
    inputValue: state.inputValue,
    sendMessage,
    setInputValue,
    addNewConversation,
    loadConversation,
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
