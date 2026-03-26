import React, { createContext, useContext, useState, type ReactNode } from 'react';
import type { Exercise, PoseDetectionResult, Landmark } from '@/types';

interface PoseContextType {
  currentExercise: Exercise | null;
  setCurrentExercise: (exercise: Exercise | null) => void;
  detectionResult: PoseDetectionResult | null;
  setDetectionResult: (result: PoseDetectionResult | null) => void;
  isDetecting: boolean;
  setIsDetecting: (detecting: boolean) => void;
  accuracy: number;
  setAccuracy: (accuracy: number) => void;
  landmarks: Landmark[];
  setLandmarks: (landmarks: Landmark[]) => void;
  resetPoseState: () => void;
}

const PoseContext = createContext<PoseContextType | undefined>(undefined);

export const PoseProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [currentExercise, setCurrentExercise] = useState<Exercise | null>(null);
  const [detectionResult, setDetectionResult] = useState<PoseDetectionResult | null>(null);
  const [isDetecting, setIsDetecting] = useState(false);
  const [accuracy, setAccuracy] = useState(0);
  const [landmarks, setLandmarks] = useState<Landmark[]>([]);

  const resetPoseState = () => {
    setDetectionResult(null);
    setIsDetecting(false);
    setAccuracy(0);
    setLandmarks([]);
  };

  return (
    <PoseContext.Provider
      value={{
        currentExercise,
        setCurrentExercise,
        detectionResult,
        setDetectionResult,
        isDetecting,
        setIsDetecting,
        accuracy,
        setAccuracy,
        landmarks,
        setLandmarks,
        resetPoseState,
      }}
    >
      {children}
    </PoseContext.Provider>
  );
};

export const usePose = () => {
  const context = useContext(PoseContext);
  if (context === undefined) {
    throw new Error('usePose must be used within a PoseProvider');
  }
  return context;
};
