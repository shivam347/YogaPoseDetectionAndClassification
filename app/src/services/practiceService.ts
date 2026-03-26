import api from './api';
import type { ApiResponse, PracticeSession, PracticeStatistics } from '@/types';

export const practiceService = {
  savePractice: async (data: {
    exercise_id: number;
    accuracy_percentage?: number;
    duration_seconds?: number;
    pose_detected?: string;
    feedback?: string;
  }): Promise<ApiResponse<{ session_id: number; practiced_at: string }>> => {
    const response = await api.post<ApiResponse<{ session_id: number; practiced_at: string }>>('/practice', data);
    return response.data;
  },

  getPracticeHistory: async (params?: { limit?: number; offset?: number }): Promise<ApiResponse<{
    sessions: PracticeSession[];
    total: number;
    statistics: PracticeStatistics;
  }>> => {
    const queryParams = new URLSearchParams();
    if (params?.limit) queryParams.append('limit', params.limit.toString());
    if (params?.offset) queryParams.append('offset', params.offset.toString());
    
    const response = await api.get<ApiResponse<{
      sessions: PracticeSession[];
      total: number;
      statistics: PracticeStatistics;
    }>>(`/practice/history?${queryParams.toString()}`);
    return response.data;
  },

  getStatistics: async (): Promise<ApiResponse<PracticeStatistics>> => {
    const response = await api.get<ApiResponse<PracticeStatistics>>('/practice/statistics');
    return response.data;
  },
};
