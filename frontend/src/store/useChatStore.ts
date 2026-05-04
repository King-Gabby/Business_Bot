import { create } from 'zustand';
import type { Message, ChatResponse } from '../types/chat';
import { chatApi } from '../services/api';
import axios from 'axios';

interface ChatStore {
  messages: Message[];
  loading: boolean;
  state: any;
  ui: ChatResponse['ui'];
  options: string[];
  userId: string;
  businessId: string;
  businessName: string;
  card: ChatResponse['card'];
  
  setBusinessId: (id: string) => void;
  fetchBusinessInfo: (id: string) => Promise<void>;
  initSession: () => Promise<void>;
  sendMessage: (text: string, silent?: boolean) => Promise<void>;
  addMessage: (message: Message) => void;
  handleAction: (action: string) => Promise<void>;
  resetChat: () => void;
}

export const useChatStore = create<ChatStore>((set, get) => ({
  messages: [],
  loading: false,
  state: null,
  ui: { show_input: true, lock_input: false },
  options: [],
  userId: 'user_' + Math.random().toString(36).substr(2, 9),
  businessId: 'idayat',
  businessName: 'AI Shopping Assistant',
  card: null,

  setBusinessId: (id) => set({ businessId: id }),

  fetchBusinessInfo: async (id) => {
    try {
      const res = await axios.get(`http://localhost:8001/business/${id}`);
      set({ businessName: res.data.name });
    } catch (err) {
      console.error('Failed to fetch business info:', err);
    }
  },

  addMessage: (message) => set((state) => ({ 
    messages: [...state.messages, message] 
  })),

  resetChat: () => set({
    messages: [],
    state: null,
    ui: { show_input: true, lock_input: false },
    options: [],
    card: null,
    loading: false
  }),

  initSession: async () => {
    const { businessId, addMessage } = get();
    set({ loading: true });
    try {
      const response = await chatApi.initChat(businessId);
      set({ 
        state: response.state,
        options: response.options || [],
        card: response.card || null,
        ui: response.ui || { show_input: true, lock_input: false },
        loading: false
      });
      if (response.reply) {
        addMessage({
          id: Date.now().toString(),
          sender: 'bot',
          text: response.reply,
          timestamp: Date.now(),
        });
      }
    } catch (error) {
      console.error('Failed to init session:', error);
      set({ loading: false });
    }
  },

  sendMessage: async (text, silent = false) => {
    const { userId, businessId, addMessage, state: currentState } = get();
    
    if (!silent) {
      addMessage({
        id: Date.now().toString(),
        sender: 'user',
        text,
        timestamp: Date.now(),
      });
    }

    set({ loading: true });

    try {
      const response = await chatApi.sendMessage(userId, text, businessId, currentState);
      
      set({ 
        state: response.state,
        options: response.options || [],
        card: response.card || null,
        ui: response.ui || { show_input: true, lock_input: false },
        loading: false
      });

      if (response.reply) {
        addMessage({
          id: (Date.now() + 1).toString(),
          sender: 'bot',
          text: response.reply,
          timestamp: Date.now(),
        });
      }
    } catch (error) {
      console.error('Failed to send message:', error);
      set({ loading: false });
      if (!silent) {
        addMessage({
          id: (Date.now() + 1).toString(),
          sender: 'bot',
          text: "I'm having trouble connecting to the store right now. Please try again later.",
          timestamp: Date.now(),
        });
      }
    }
  },

  handleAction: async (action) => {
    await get().sendMessage(action);
  },
}));
