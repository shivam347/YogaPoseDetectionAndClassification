import { useRef, useEffect } from 'react';
import type { Landmark } from '@/types';

interface PoseCanvasProps {
  landmarks: Landmark[];
  width?: number;
  height?: number;
}

// MediaPipe Pose Connections
const POSE_CONNECTIONS = [
  [0, 1], [0, 2], [1, 3], [2, 4], [3, 5], [4, 6], // Face
  [5, 6], [5, 7], [6, 8], [7, 9], [8, 10], // Upper body
  [5, 11], [6, 12], [11, 12], [11, 13], [12, 14], // Shoulders and arms
  [13, 15], [14, 16], [15, 17], [16, 18], [15, 19], [16, 20], // Hands
  [11, 23], [12, 24], [23, 24], [23, 25], [24, 26], // Hips and legs
  [25, 27], [26, 28], [27, 29], [28, 30], [29, 31], [30, 32], // Feet
];

const PoseCanvas = ({ landmarks, width = 640, height = 480 }: PoseCanvasProps) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    if (!canvasRef.current || landmarks.length === 0) return;

    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Clear canvas
    ctx.clearRect(0, 0, width, height);

    // Draw connections
    ctx.strokeStyle = '#10b981';
    ctx.lineWidth = 3;

    POSE_CONNECTIONS.forEach(([start, end]) => {
      if (landmarks[start] && landmarks[end]) {
        const startPoint = landmarks[start];
        const endPoint = landmarks[end];

        if (startPoint.visibility > 0.5 && endPoint.visibility > 0.5) {
          ctx.beginPath();
          ctx.moveTo(startPoint.x * width, startPoint.y * height);
          ctx.lineTo(endPoint.x * width, endPoint.y * height);
          ctx.stroke();
        }
      }
    });

    // Draw landmarks
    landmarks.forEach((landmark) => {
      if (landmark.visibility > 0.5) {
        const x = landmark.x * width;
        const y = landmark.y * height;

        // Draw point
        ctx.beginPath();
        ctx.arc(x, y, 6, 0, 2 * Math.PI);
        ctx.fillStyle = '#3b82f6';
        ctx.fill();

        // Draw border
        ctx.beginPath();
        ctx.arc(x, y, 6, 0, 2 * Math.PI);
        ctx.strokeStyle = '#ffffff';
        ctx.lineWidth = 2;
        ctx.stroke();

        // Draw index number (optional, for debugging)
        // ctx.fillStyle = '#ffffff';
        // ctx.font = '10px Arial';
        // ctx.fillText(index.toString(), x + 8, y + 3);
      }
    });
  }, [landmarks, width, height]);

  if (landmarks.length === 0) return null;

  return (
    <canvas
      ref={canvasRef}
      width={width}
      height={height}
      className="absolute inset-0 w-full h-full pointer-events-none"
      style={{ zIndex: 10 }}
    />
  );
};

export default PoseCanvas;
