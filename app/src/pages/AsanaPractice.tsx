import { useEffect, useState, useCallback, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { exerciseService } from '@/services/exerciseService';
import { poseService } from '@/services/poseService';
import { practiceService } from '@/services/practiceService';
import { usePose } from '@/context/PoseContext';
import type { Exercise, PoseDetectionResult } from '@/types';
import CameraFeed from '@/components/pose/CameraFeed';
import PoseCanvas from '@/components/pose/PoseCanvas';
import AccuracyMeter from '@/components/pose/AccuracyMeter';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Skeleton } from '@/components/ui/skeleton';
import { 
  ArrowLeft, 
  Clock, 
  Play, 
  Pause, 
  RotateCcw,
  Check,
  AlertCircle,
  Save
} from 'lucide-react';
import { toast } from 'sonner';

const AsanaPractice = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { setCurrentExercise } = usePose();
  const [exercise, setExercise] = useState<Exercise | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isPracticing, setIsPracticing] = useState(false);
  const [isPaused, setIsPaused] = useState(false);
  const [elapsedTime, setElapsedTime] = useState(0);
  const [detectionResult, setDetectionResult] = useState<PoseDetectionResult | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [sessionAccuracy, setSessionAccuracy] = useState<number[]>([]);
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);

  useEffect(() => {
    if (id) {
      loadExercise(parseInt(id));
    }
    return () => {
      if (timerRef.current) {
        clearInterval(timerRef.current);
      }
    };
  }, [id]);

  useEffect(() => {
    if (isPracticing && !isPaused) {
      timerRef.current = setInterval(() => {
        setElapsedTime(prev => prev + 1);
      }, 1000);
    } else {
      if (timerRef.current) {
        clearInterval(timerRef.current);
      }
    }
    return () => {
      if (timerRef.current) {
        clearInterval(timerRef.current);
      }
    };
  }, [isPracticing, isPaused]);

  const loadExercise = async (exerciseId: number) => {
    try {
      setIsLoading(true);
      const response = await exerciseService.getExercise(exerciseId);
      
      if (response.success) {
        setExercise(response.data);
        setCurrentExercise(response.data);
      }
    } catch (error) {
      toast.error('Failed to load exercise');
    } finally {
      setIsLoading(false);
    }
  };

  const handleFrame = useCallback(async (imageSrc: string) => {
    if (!exercise?.pose_key || isProcessing) return;

    setIsProcessing(true);
    try {
      const response = await poseService.detectPose(imageSrc, exercise.pose_key);
      if (response.success) {
        setDetectionResult(response.data);
        if (response.data.accuracy_percentage > 0) {
          setSessionAccuracy(prev => [...prev, response.data.accuracy_percentage]);
        }
      }
    } catch (error) {
      console.error('Pose detection error:', error);
    } finally {
      setIsProcessing(false);
    }
  }, [exercise, isProcessing]);

  const startPractice = () => {
    setIsPracticing(true);
    setIsPaused(false);
    setElapsedTime(0);
    setSessionAccuracy([]);
  };

  const pausePractice = () => {
    setIsPaused(!isPaused);
  };

  const stopPractice = () => {
    setIsPracticing(false);
    setIsPaused(false);
    if (timerRef.current) {
      clearInterval(timerRef.current);
    }
  };

  const saveSession = async () => {
    if (!exercise) return;

    const avgAccuracy = sessionAccuracy.length > 0
      ? sessionAccuracy.reduce((a, b) => a + b, 0) / sessionAccuracy.length
      : 0;

    try {
      await practiceService.savePractice({
        exercise_id: exercise.id,
        accuracy_percentage: avgAccuracy,
        duration_seconds: elapsedTime,
        pose_detected: detectionResult?.pose_detected || exercise.name,
        feedback: detectionResult?.feedback,
      });
      
      toast.success('Practice session saved!');
      navigate('/dashboard');
    } catch (error) {
      toast.error('Failed to save session');
    }
  };

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  const getAverageAccuracy = () => {
    if (sessionAccuracy.length === 0) return 0;
    return sessionAccuracy.reduce((a, b) => a + b, 0) / sessionAccuracy.length;
  };

  if (isLoading) {
    return (
      <div className="min-h-screen pt-24 pb-12 px-4">
        <div className="max-w-6xl mx-auto">
          <Skeleton className="h-12 w-48 mb-8" />
          <div className="grid lg:grid-cols-2 gap-8">
            <Skeleton className="h-96 rounded-2xl" />
            <Skeleton className="h-96 rounded-2xl" />
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen pt-24 pb-12 px-4 bg-gradient-to-br from-sage-50 via-white to-lavender-50">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-8">
          <div className="flex items-center gap-4">
            <Button 
              variant="ghost" 
              onClick={() => navigate(-1)}
            >
              <ArrowLeft className="w-4 h-4 mr-2" />
              Back
            </Button>
            <div>
              <h1 className="text-2xl md:text-3xl font-serif font-bold text-gray-900">
                {exercise?.name}
              </h1>
              {exercise?.sanskrit_name && (
                <p className="text-gray-500 italic">{exercise.sanskrit_name}</p>
              )}
            </div>
          </div>
          
          {isPracticing && (
            <div className="flex items-center gap-4">
              <Badge variant="secondary" className="text-lg px-4 py-2">
                <Clock className="w-4 h-4 mr-2" />
                {formatTime(elapsedTime)}
              </Badge>
            </div>
          )}
        </div>

        {/* Main Content */}
        <div className="grid lg:grid-cols-2 gap-8">
          {/* Camera Feed */}
          <div className="space-y-4">
            <Card className="border-0 shadow-xl overflow-hidden">
              <CardContent className="p-0 relative">
                <CameraFeed 
                  onFrame={handleFrame}
                  isProcessing={isProcessing}
                />
                {detectionResult?.landmarks && (
                  <PoseCanvas 
                    landmarks={detectionResult.landmarks}
                    width={640}
                    height={480}
                  />
                )}
              </CardContent>
            </Card>

            {/* Controls */}
            <div className="flex justify-center gap-4">
              {!isPracticing ? (
                <Button
                  onClick={startPractice}
                  size="lg"
                  className="bg-gradient-to-r from-sage-500 to-lavender-500 text-white hover:opacity-90 rounded-full px-8"
                >
                  <Play className="w-5 h-5 mr-2" />
                  Start Practice
                </Button>
              ) : (
                <>
                  <Button
                    onClick={pausePractice}
                    variant="outline"
                    size="lg"
                    className="rounded-full"
                  >
                    {isPaused ? <Play className="w-5 h-5 mr-2" /> : <Pause className="w-5 h-5 mr-2" />}
                    {isPaused ? 'Resume' : 'Pause'}
                  </Button>
                  <Button
                    onClick={stopPractice}
                    variant="destructive"
                    size="lg"
                    className="rounded-full"
                  >
                    <RotateCcw className="w-5 h-5 mr-2" />
                    Stop
                  </Button>
                </>
              )}
            </div>
          </div>

          {/* Feedback Panel */}
          <div className="space-y-4">
            {/* Accuracy Meter */}
            <Card className="border-0 shadow-lg">
              <CardContent className="p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">
                  Pose Accuracy
                </h3>
                <div className="flex justify-center">
                  <AccuracyMeter 
                    accuracy={detectionResult?.accuracy_percentage || 0}
                    size="lg"
                  />
                </div>
              </CardContent>
            </Card>

            {/* Current Detection */}
            {detectionResult && (
              <Card className="border-0 shadow-lg">
                <CardContent className="p-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">
                    Detection Result
                  </h3>
                  <div className="space-y-3">
                    <div className="flex justify-between">
                      <span className="text-gray-600">Detected Pose:</span>
                      <span className="font-medium">{detectionResult.pose_detected}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Confidence:</span>
                      <span className="font-medium">
                        {(detectionResult.confidence * 100).toFixed(1)}%
                      </span>
                    </div>
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Feedback */}
            {detectionResult?.feedback && (
              <Card className="border-0 shadow-lg">
                <CardContent className="p-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">
                    Feedback
                  </h3>
                  <div className="flex items-start gap-3">
                    <div className="w-8 h-8 bg-sage-100 rounded-full flex items-center justify-center flex-shrink-0">
                      <Check className="w-4 h-4 text-sage-600" />
                    </div>
                    <p className="text-gray-700">{detectionResult.feedback}</p>
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Corrections */}
            {detectionResult?.corrections && detectionResult.corrections.length > 0 && (
              <Card className="border-0 shadow-lg">
                <CardContent className="p-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">
                    Suggestions
                  </h3>
                  <div className="space-y-2">
                    {detectionResult.corrections.map((correction, index) => (
                      <div 
                        key={index}
                        className="flex items-start gap-3 p-3 bg-yellow-50 rounded-xl"
                      >
                        <AlertCircle className="w-5 h-5 text-yellow-600 flex-shrink-0 mt-0.5" />
                        <span className="text-gray-700 text-sm">{correction}</span>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Session Summary */}
            {sessionAccuracy.length > 0 && (
              <Card className="border-0 shadow-lg bg-gradient-to-r from-sage-50 to-lavender-50">
                <CardContent className="p-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">
                    Session Summary
                  </h3>
                  <div className="grid grid-cols-2 gap-4 mb-4">
                    <div className="text-center p-3 bg-white rounded-xl">
                      <p className="text-2xl font-bold text-sage-600">
                        {getAverageAccuracy().toFixed(1)}%
                      </p>
                      <p className="text-sm text-gray-500">Avg Accuracy</p>
                    </div>
                    <div className="text-center p-3 bg-white rounded-xl">
                      <p className="text-2xl font-bold text-lavender-600">
                        {formatTime(elapsedTime)}
                      </p>
                      <p className="text-sm text-gray-500">Duration</p>
                    </div>
                  </div>
                  <Button
                    onClick={saveSession}
                    className="w-full bg-gradient-to-r from-sage-500 to-lavender-500 text-white hover:opacity-90"
                  >
                    <Save className="w-4 h-4 mr-2" />
                    Save Session
                  </Button>
                </CardContent>
              </Card>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default AsanaPractice;
