import { apiClient, setAccessToken } from './client';
import type { LoginRequest, LoginResponse, User } from '../types';

export const authApi = {
  login: async (data: LoginRequest): Promise<LoginResponse> => {
    const response = await apiClient.post<LoginResponse>('/auth/login', data, {
      withCredentials: true, // Receive refresh token cookie
    });
    setAccessToken(response.data.access_token);
    return response.data;
  },

  logout: async (): Promise<void> => {
    try {
      await apiClient.post('/auth/logout', {}, {
        withCredentials: true,
      });
    } finally {
      setAccessToken(null);
    }
  },

  refresh: async (): Promise<{ access_token: string; user: User }> => {
    const response = await apiClient.post('/auth/refresh', {}, {
      withCredentials: true,
    });
    setAccessToken(response.data.access_token);
    return response.data;
  },

  me: async (): Promise<User> => {
    const response = await apiClient.get<User>('/auth/me');
    return response.data;
  },
};
