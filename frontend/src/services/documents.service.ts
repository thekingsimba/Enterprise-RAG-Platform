import apiClient from './api';
import { Document } from '@/types';

export const documentsService = {
  async getDocuments(skip = 0, limit = 20): Promise<Document[]> {
    const response = await apiClient.get<Document[]>('/documents/', {
      params: { skip, limit },
    });
    return response.data;
  },

  async getDocument(id: string): Promise<Document> {
    const response = await apiClient.get<Document>(`/documents/${id}`);
    return response.data;
  },

  async uploadDocument(file: File, title?: string, description?: string): Promise<Document> {
    const formData = new FormData();
    formData.append('file', file);
    if (title) formData.append('title', title);
    if (description) formData.append('description', description);

    const response = await apiClient.post<Document>('/documents/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  async updateDocument(
    id: string,
    data: { title?: string; description?: string; tags?: string[] }
  ): Promise<Document> {
    const response = await apiClient.put<Document>(`/documents/${id}`, data);
    return response.data;
  },

  async deleteDocument(id: string): Promise<void> {
    await apiClient.delete(`/documents/${id}`);
  },
};

