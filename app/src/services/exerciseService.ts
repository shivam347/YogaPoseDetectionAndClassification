import api from './api';
import type { ApiResponse, Exercise, PainCategory } from '@/types';

export const exerciseService = {
  getExercises: async (filters?: { pain_type?: string; difficulty?: string; search?: string }): Promise<ApiResponse<Exercise[]>> => {
    const params = new URLSearchParams();
    if (filters?.pain_type) params.append('pain_type', filters.pain_type);
    if (filters?.difficulty) params.append('difficulty', filters.difficulty);
    if (filters?.search) params.append('search', filters.search);
    
    const response = await api.get<ApiResponse<Exercise[]>>(`/exercises?${params.toString()}`);
    return response.data;
  },

  getExercise: async (id: number): Promise<ApiResponse<Exercise>> => {
    const response = await api.get<ApiResponse<Exercise>>(`/exercises/${id}`);
    return response.data;
  },

  getPainCategories: async (): Promise<ApiResponse<PainCategory[]>> => {
    const response = await api.get<ApiResponse<PainCategory[]>>('/exercises/pain-categories');
    return response.data;
  },

  getExercisesByCategory: async (categoryId: number): Promise<ApiResponse<{ category: PainCategory; exercises: Exercise[] }>> => {
    const response = await api.get<ApiResponse<{ category: PainCategory; exercises: Exercise[] }>>(`/exercises/pain-categories/${categoryId}/exercises`);
    return response.data;
  },
};
