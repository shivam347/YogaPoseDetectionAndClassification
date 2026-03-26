import api from './api';
import type { ApiResponse, PoseDetectionResult, Landmark } from '@/types';

export const poseService = {
  detectPose: async (imageBase64: string, targetPose?: string): Promise<ApiResponse<PoseDetectionResult>> => {
    const response = await api.post<ApiResponse<PoseDetectionResult>>('/pose/detect', {
      image: imageBase64,
      target_pose: targetPose,
    });
    return response.data;
  },

  classifyPose: async (landmarks: Landmark[]): Promise<ApiResponse<any>> => {
    const response = await api.post<ApiResponse<any>>('/pose/classify', {
      landmarks: landmarks.flatMap(lm => [lm.x, lm.y, lm.z, lm.visibility]),
    });
    return response.data;
  },

  extractLandmarks: async (imageBase64: string): Promise<ApiResponse<{ landmarks: Landmark[]; landmark_count: number }>> => {
    const response = await api.post<ApiResponse<{ landmarks: Landmark[]; landmark_count: number }>>('/pose/landmarks', {
      image: imageBase64,
    });
    return response.data;
  },

  getSupportedPoses: async (): Promise<ApiResponse<{ key: string; name: string }[]>> => {
    const response = await api.get<ApiResponse<{ key: string; name: string }[]>>('/pose/poses');
    return response.data;
  },

  getPoseFeedback: async (landmarks: Landmark[], targetPose: string): Promise<ApiResponse<{ accuracy_percentage: number; feedback: string; corrections: string[] }>> => {
    const response = await api.post<ApiResponse<{ accuracy_percentage: number; feedback: string; corrections: string[] }>>('/pose/feedback', {
      landmarks: landmarks.flatMap(lm => [lm.x, lm.y, lm.z, lm.visibility]),
      target_pose: targetPose,
    });
    return response.data;
  },
};
