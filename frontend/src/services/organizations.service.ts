import apiClient from './api';
import { Organization } from '@/types';

export const organizationsService = {
  async getOrganizations(skip = 0, limit = 20): Promise<Organization[]> {
    const response = await apiClient.get<Organization[]>('/organizations/', {
      params: { skip, limit },
    });
    return response.data;
  },

  async getOrganization(id: string): Promise<Organization> {
    const response = await apiClient.get<Organization>(`/organizations/${id}`);
    return response.data;
  },

  async createOrganization(data: {
    name: string;
    slug: string;
    tier?: string;
  }): Promise<Organization> {
    const response = await apiClient.post<Organization>('/organizations/', data);
    return response.data;
  },

  async updateOrganization(
    id: string,
    data: {
      name?: string;
      tier?: string;
      is_active?: boolean;
      max_documents?: number;
      max_storage_mb?: number;
      max_users?: number;
    }
  ): Promise<Organization> {
    const response = await apiClient.put<Organization>(`/organizations/${id}`, data);
    return response.data;
  },

  async deleteOrganization(id: string): Promise<void> {
    await apiClient.delete(`/organizations/${id}`);
  },
};

