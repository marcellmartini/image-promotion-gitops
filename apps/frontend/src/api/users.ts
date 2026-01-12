import { apiClient } from './client';
import type { User, UserCreate, UserUpdate, UserListResponse } from '../types';

export const usersApi = {
  list: async (skip = 0, limit = 100): Promise<UserListResponse> => {
    const response = await apiClient.get<UserListResponse>('/users', {
      params: { skip, limit },
    });
    return response.data;
  },

  get: async (id: string): Promise<User> => {
    const response = await apiClient.get<User>(`/users/${id}`);
    return response.data;
  },

  create: async (data: UserCreate): Promise<User> => {
    const response = await apiClient.post<User>('/users', data);
    return response.data;
  },

  update: async (id: string, data: UserUpdate): Promise<User> => {
    const response = await apiClient.put<User>(`/users/${id}`, data);
    return response.data;
  },

  delete: async (id: string): Promise<void> => {
    await apiClient.delete(`/users/${id}`);
  },
};
