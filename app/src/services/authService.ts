import api from './api';
import type { ApiResponse, AuthResponse, User } from '@/types';

export const authService = {
  register: async (name: string, email: string, password: string): Promise<AuthResponse> => {
    const response = await api.post<AuthResponse>('/auth/register', {
      name,
      email,
      password,
    });
    return response.data;
  },

  login: async (email: string, password: string): Promise<AuthResponse> => {
    const response = await api.post<AuthResponse>('/auth/login', {
      email,
      password,
    });
    return response.data;
  },

  getProfile: async (): Promise<ApiResponse<User & { total_sessions: number; average_accuracy: number }>> => {
    const response = await api.get<ApiResponse<User & { total_sessions: number; average_accuracy: number }>>('/auth/profile');
    return response.data;
  },

  updateProfile: async (data: { name?: string; avatar_url?: string }): Promise<ApiResponse<User>> => {
    const response = await api.put<ApiResponse<User>>('/auth/profile', data);
    return response.data;
  },

  logout: () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  },

  setAuthData: (token: string, user: any) => {
    localStorage.setItem('token', token);
    localStorage.setItem('user', JSON.stringify(user));
  },

  getToken: (): string | null => {
    return localStorage.getItem('token');
  },

  getUser: (): any | null => {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
  },
};
