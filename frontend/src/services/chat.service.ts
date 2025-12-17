import apiClient from './api';
import { Conversation, Message, ChatRequest, ChatResponse } from '@/types';

export const chatService = {
  async getConversations(skip = 0, limit = 20): Promise<Conversation[]> {
    const response = await apiClient.get<Conversation[]>('/chat/conversations', {
      params: { skip, limit },
    });
    return response.data;
  },

  async getConversation(id: string): Promise<Conversation> {
    const response = await apiClient.get<Conversation>(`/chat/conversations/${id}`);
    return response.data;
  },

  async createConversation(title: string): Promise<Conversation> {
    const response = await apiClient.post<Conversation>('/chat/conversations', { title });
    return response.data;
  },

  async updateConversation(
    id: string,
    data: { title?: string; is_archived?: boolean }
  ): Promise<Conversation> {
    const response = await apiClient.put<Conversation>(`/chat/conversations/${id}`, data);
    return response.data;
  },

  async deleteConversation(id: string): Promise<void> {
    await apiClient.delete(`/chat/conversations/${id}`);
  },

  async sendMessage(request: ChatRequest): Promise<ChatResponse> {
    const response = await apiClient.post<ChatResponse>('/chat/chat', request);
    return response.data;
  },

  async sendMessageWithWorkflow(request: ChatRequest): Promise<ChatResponse> {
    const response = await apiClient.post<ChatResponse>('/chat/chat/workflow', request);
    return response.data;
  },

  // Streaming is handled separately in the component
  getStreamUrl(): string {
    return `${apiClient.defaults.baseURL}/chat/chat/stream`;
  },
};

