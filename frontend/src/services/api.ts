import axios from 'axios';
import type { ChatResponse } from '../types/chat';

const API_BASE_URL = `http://${window.location.hostname}:8001`; 

export const chatApi = {
  sendMessage: async (userId: string, message: string, businessId: string, state: any = {}): Promise<ChatResponse> => {
    const response = await axios.post(`${API_BASE_URL}/chat`, {
      user_id: userId,
      message: message,
      business_id: businessId,
      state: state
    });
    return response.data;
  },
};
