import apiClient from './api';
import { AnalyticsOverview, UsageMetric, User } from '@/types';

export const adminService = {
  async getAnalyticsOverview(): Promise<AnalyticsOverview> {
    const response = await apiClient.get<AnalyticsOverview>('/admin/analytics/overview');
    return response.data;
  },

  async getOrganizationAnalytics(skip = 0, limit = 20): Promise<any[]> {
    const response = await apiClient.get('/admin/analytics/organizations', {
      params: { skip, limit },
    });
    return response.data;
  },

  async getUsageAnalytics(days = 30): Promise<UsageMetric[]> {
    const response = await apiClient.get<UsageMetric[]>('/admin/analytics/usage', {
      params: { days },
    });
    return response.data;
  },

  async getAllUsers(skip = 0, limit = 50): Promise<User[]> {
    const response = await apiClient.get<User[]>('/admin/users', {
      params: { skip, limit },
    });
    return response.data;
  },

  async activateUser(userId: string): Promise<any> {
    const response = await apiClient.put(`/admin/users/${userId}/activate`);
    return response.data;
  },

  async deactivateUser(userId: string): Promise<any> {
    const response = await apiClient.put(`/admin/users/${userId}/deactivate`);
    return response.data;
  },

  async getDocumentStats(): Promise<any> {
    const response = await apiClient.get('/admin/documents/stats');
    return response.data;
  },
};

