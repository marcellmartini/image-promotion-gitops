import { create } from 'zustand';
import { authApi } from '../api';
import { getAccessToken, getRefreshToken } from '../api/client';
import type { User } from '../types';

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  checkAuth: () => Promise<void>;
  clearError: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  isAuthenticated: false,
  isLoading: true,
  error: null,

  login: async (email: string, password: string) => {
    set({ isLoading: true, error: null });
    try {
      const response = await authApi.login({ email, password });
      set({
        user: response.user,
        isAuthenticated: true,
        isLoading: false,
        error: null,
      });
    } catch (err) {
      const message = (err as { response?: { data?: { detail?: string } } })
        ?.response?.data?.detail || 'Login failed';
      set({ isLoading: false, error: message });
      throw err;
    }
  },

  logout: async () => {
    try {
      await authApi.logout();
    } finally {
      set({
        user: null,
        isAuthenticated: false,
        isLoading: false,
        error: null,
      });
    }
  },

  checkAuth: async () => {
    // Check if we have stored tokens
    const accessToken = getAccessToken();
    const refreshToken = getRefreshToken();

    if (!accessToken && !refreshToken) {
      set({
        user: null,
        isAuthenticated: false,
        isLoading: false,
      });
      return;
    }

    set({ isLoading: true });
    try {
      // Try to get current user with existing access token
      const user = await authApi.me();
      set({
        user,
        isAuthenticated: true,
        isLoading: false,
      });
    } catch {
      // Access token might be expired, try to refresh
      try {
        const response = await authApi.refresh();
        set({
          user: response.user,
          isAuthenticated: true,
          isLoading: false,
        });
      } catch {
        set({
          user: null,
          isAuthenticated: false,
          isLoading: false,
        });
      }
    }
  },

  clearError: () => set({ error: null }),
}));
