import { useEffect, useState } from 'react';
import { Progress } from '@/components/ui/progress';

interface AccuracyMeterProps {
  accuracy: number;
  size?: 'sm' | 'md' | 'lg';
  showLabel?: boolean;
}

const AccuracyMeter = ({ accuracy, size = 'md', showLabel = true }: AccuracyMeterProps) => {
  const [displayAccuracy, setDisplayAccuracy] = useState(0);

  useEffect(() => {
    // Animate the accuracy value
    const duration = 500;
    const startTime = Date.now();
    const startValue = displayAccuracy;
    
    const animate = () => {
      const elapsed = Date.now() - startTime;
      const progress = Math.min(elapsed / duration, 1);
      
      // Easing function
      const easeOutQuart = 1 - Math.pow(1 - progress, 4);
      
      const currentValue = startValue + (accuracy - startValue) * easeOutQuart;
      setDisplayAccuracy(currentValue);
      
      if (progress < 1) {
        requestAnimationFrame(animate);
      }
    };
    
    requestAnimationFrame(animate);
  }, [accuracy]);

  const getColor = (value: number) => {
    if (value >= 90) return 'text-green-500';
    if (value >= 75) return 'text-yellow-500';
    if (value >= 50) return 'text-orange-500';
    return 'text-red-500';
  };



  const getSizeClasses = () => {
    switch (size) {
      case 'sm':
        return 'w-24';
      case 'lg':
        return 'w-48';
      default:
        return 'w-32';
    }
  };

  return (
    <div className={`flex flex-col items-center ${getSizeClasses()}`}>
      {/* Circular Progress */}
      <div className="relative">
        <svg className="transform -rotate-90" viewBox="0 0 100 100">
          {/* Background circle */}
          <circle
            cx="50"
            cy="50"
            r="45"
            fill="none"
            stroke="#e5e7eb"
            strokeWidth="8"
          />
          {/* Progress circle */}
          <circle
            cx="50"
            cy="50"
            r="45"
            fill="none"
            stroke="currentColor"
            strokeWidth="8"
            strokeLinecap="round"
            strokeDasharray={`${2 * Math.PI * 45}`}
            strokeDashoffset={`${2 * Math.PI * 45 * (1 - displayAccuracy / 100)}`}
            className={`transition-all duration-300 ${getColor(displayAccuracy)}`}
          />
        </svg>
        
        {/* Center text */}
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className={`text-2xl font-bold ${getColor(displayAccuracy)}`}>
            {Math.round(displayAccuracy)}%
          </span>
          {showLabel && (
            <span className="text-xs text-gray-500">Accuracy</span>
          )}
        </div>
      </div>

      {/* Linear Progress Bar */}
      <div className="w-full mt-4">
        <Progress 
          value={displayAccuracy} 
          className="h-2"
        />
      </div>

      {/* Feedback Text */}
      {showLabel && (
        <p className={`mt-2 text-sm font-medium ${getColor(displayAccuracy)}`}>
          {displayAccuracy >= 90 ? 'Excellent!' : 
           displayAccuracy >= 75 ? 'Good Job!' : 
           displayAccuracy >= 50 ? 'Keep Trying!' : 'Need Improvement'}
        </p>
      )}
    </div>
  );
};

export default AccuracyMeter;
