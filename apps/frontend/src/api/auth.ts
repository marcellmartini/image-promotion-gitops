import { apiClient, setAccessToken, setRefreshToken, getRefreshToken, clearTokens } from './client';
import type { LoginRequest, LoginResponse, User } from '../types';

export const authApi = {
  login: async (data: LoginRequest): Promise<LoginResponse> => {
    const response = await apiClient.post<LoginResponse>('/auth/login', data);
    setAccessToken(response.data.access_token);
    setRefreshToken(response.data.refresh_token);
    return response.data;
  },

  logout: async (): Promise<void> => {
    try {
      await apiClient.post('/auth/logout');
    } finally {
      clearTokens();
    }
  },

  refresh: async (): Promise<{ access_token: string; user: User }> => {
    const refreshToken = getRefreshToken();
    if (!refreshToken) {
      throw new Error('No refresh token');
    }
    const response = await apiClient.post('/auth/refresh', {
      refresh_token: refreshToken,
    });
    setAccessToken(response.data.access_token);
    return response.data;
  },

  me: async (): Promise<User> => {
    const response = await apiClient.get<User>('/auth/me');
    return response.data;
  },
};
