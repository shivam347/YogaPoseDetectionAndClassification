// User Types
export interface User {
  id: number;
  name: string;
  email: string;
  avatar_url?: string;
  created_at?: string;
  is_active?: boolean;
}

export interface AuthResponse {
  success: boolean;
  message: string;
  data: {
    user_id: number;
    name: string;
    email: string;
    token: string;
  };
}

// Exercise Types
export interface PainCategory {
  id: number;
  name: string;
  description: string;
  icon: string;
  color: string;
}

export interface Exercise {
  id: number;
  name: string;
  sanskrit_name?: string;
  description: string;
  benefits?: string[];
  instructions?: string[];
  difficulty_level: 'beginner' | 'intermediate' | 'advanced';
  image_url: string;
  video_url?: string;
  duration_seconds?: number;
  pose_key?: string;
  target_body_parts?: string[];
  pain_category?: PainCategory;
}

// Practice Types
export interface PracticeSession {
  id: number;
  exercise_name: string;
  accuracy_percentage: number;
  duration_seconds: number;
  pose_detected: string;
  feedback?: string;
  practiced_at: string;
}

export interface PracticeStatistics {
  total_sessions: number;
  total_minutes: number;
  average_accuracy: number;
  best_accuracy?: number;
  streak_days: number;
  top_exercises?: { name: string; count: number }[];
}

// Pose Detection Types
export interface Landmark {
  x: number;
  y: number;
  z: number;
  visibility: number;
}

export interface PoseDetectionResult {
  pose_detected: string;
  pose_class: string;
  confidence: number;
  accuracy_percentage: number;
  landmarks: Landmark[];
  feedback: string;
  corrections: string[];
  all_predictions: { pose: string; confidence: number }[];
}

export interface PosePrediction {
  pose: string;
  confidence: number;
}

// API Response Types
export interface ApiResponse<T> {
  success: boolean;
  message?: string;
  data: T;
  count?: number;
}
