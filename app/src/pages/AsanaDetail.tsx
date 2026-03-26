import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { exerciseService } from '@/services/exerciseService';
import { usePose } from '@/context/PoseContext';
import type { Exercise } from '@/types';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Skeleton } from '@/components/ui/skeleton';
import { 
  ArrowLeft, 
  Clock, 
  TrendingUp, 
  Check,
  Info,
  Camera
} from 'lucide-react';
import { toast } from 'sonner';

const AsanaDetail = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { setCurrentExercise } = usePose();
  const [exercise, setExercise] = useState<Exercise | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (id) {
      loadExercise(parseInt(id));
    }
  }, [id]);

  const loadExercise = async (exerciseId: number) => {
    try {
      setIsLoading(true);
      const response = await exerciseService.getExercise(exerciseId);
      
      if (response.success) {
        setExercise(response.data);
        setCurrentExercise(response.data);
      }
    } catch (error) {
      toast.error('Failed to load exercise details');
    } finally {
      setIsLoading(false);
    }
  };

  const getDifficultyColor = (level: string) => {
    switch (level) {
      case 'beginner':
        return 'bg-green-100 text-green-700';
      case 'intermediate':
        return 'bg-yellow-100 text-yellow-700';
      case 'advanced':
        return 'bg-red-100 text-red-700';
      default:
        return 'bg-gray-100 text-gray-700';
    }
  };

  const formatDuration = (seconds?: number) => {
    if (!seconds) return 'N/A';
    if (seconds < 60) return `${seconds} seconds`;
    return `${Math.floor(seconds / 60)} minutes`;
  };

  const handleStartPractice = () => {
    if (exercise) {
      navigate(`/practice/${exercise.id}`);
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen pt-24 pb-12 px-4">
        <div className="max-w-4xl mx-auto">
          <Skeleton className="h-8 w-32 mb-8" />
          <Skeleton className="h-96 rounded-2xl mb-8" />
          <Skeleton className="h-64 rounded-2xl" />
        </div>
      </div>
    );
  }

  if (!exercise) {
    return (
      <div className="min-h-screen pt-24 pb-12 px-4 flex items-center justify-center">
        <div className="text-center">
          <Info className="w-16 h-16 text-gray-300 mx-auto mb-4" />
          <h2 className="text-2xl font-semibold text-gray-700 mb-2">
            Exercise not found
          </h2>
          <Button onClick={() => navigate('/pain-selection')}>
            Back to Categories
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen pt-24 pb-12 px-4 bg-gradient-to-br from-sage-50 via-white to-lavender-50">
      <div className="max-w-4xl mx-auto">
        {/* Back Button */}
        <Button 
          variant="ghost" 
          className="mb-6"
          onClick={() => navigate(-1)}
        >
          <ArrowLeft className="w-4 h-4 mr-2" />
          Back
        </Button>

        {/* Hero Image */}
        <div className="relative h-80 md:h-96 rounded-3xl overflow-hidden mb-8 shadow-2xl">
          {exercise.image_url ? (
            <img
              src={exercise.image_url}
              alt={exercise.name}
              className="w-full h-full object-cover"
            />
          ) : (
            <div className="w-full h-full bg-gradient-to-br from-sage-200 to-lavender-200 flex items-center justify-center">
              <span className="text-6xl font-serif text-sage-600">
                {exercise.name.charAt(0)}
              </span>
            </div>
          )}
          
          {/* Overlay */}
          <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent" />
          
          {/* Content */}
          <div className="absolute bottom-0 left-0 right-0 p-6 md:p-8">
            <Badge className={`mb-3 ${getDifficultyColor(exercise.difficulty_level)}`}>
              {exercise.difficulty_level}
            </Badge>
            <h1 className="text-3xl md:text-4xl font-serif font-bold text-white mb-2">
              {exercise.name}
            </h1>
            {exercise.sanskrit_name && (
              <p className="text-xl text-white/80 italic">
                {exercise.sanskrit_name}
              </p>
            )}
          </div>
        </div>

        {/* Info Cards */}
        <div className="grid sm:grid-cols-3 gap-4 mb-8">
          <Card className="border-0 shadow-md">
            <CardContent className="p-4 flex items-center gap-3">
              <div className="w-10 h-10 bg-sage-100 rounded-lg flex items-center justify-center">
                <Clock className="w-5 h-5 text-sage-600" />
              </div>
              <div>
                <p className="text-sm text-gray-500">Duration</p>
                <p className="font-semibold">{formatDuration(exercise.duration_seconds)}</p>
              </div>
            </CardContent>
          </Card>

          <Card className="border-0 shadow-md">
            <CardContent className="p-4 flex items-center gap-3">
              <div className="w-10 h-10 bg-lavender-100 rounded-lg flex items-center justify-center">
                <TrendingUp className="w-5 h-5 text-lavender-600" />
              </div>
              <div>
                <p className="text-sm text-gray-500">Targets</p>
                <p className="font-semibold">
                  {exercise.target_body_parts?.length || 0} areas
                </p>
              </div>
            </CardContent>
          </Card>

          <Card className="border-0 shadow-md">
            <CardContent className="p-4 flex items-center gap-3">
              <div className="w-10 h-10 bg-yellow-100 rounded-lg flex items-center justify-center">
                <Check className="w-5 h-5 text-yellow-600" />
              </div>
              <div>
                <p className="text-sm text-gray-500">Difficulty</p>
                <p className="font-semibold capitalize">{exercise.difficulty_level}</p>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Description */}
        <Card className="border-0 shadow-lg mb-8">
          <CardContent className="p-6 md:p-8">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">
              About this Pose
            </h2>
            <p className="text-gray-600 leading-relaxed">
              {exercise.description}
            </p>
          </CardContent>
        </Card>

        {/* Benefits */}
        {exercise.benefits && exercise.benefits.length > 0 && (
          <Card className="border-0 shadow-lg mb-8">
            <CardContent className="p-6 md:p-8">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">
                Benefits
              </h2>
              <div className="grid sm:grid-cols-2 gap-3">
                {exercise.benefits.map((benefit, index) => (
                  <div 
                    key={index}
                    className="flex items-start gap-3 p-3 bg-sage-50 rounded-xl"
                  >
                    <div className="w-6 h-6 bg-sage-500 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                      <Check className="w-4 h-4 text-white" />
                    </div>
                    <span className="text-gray-700">{benefit}</span>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        )}

        {/* Instructions */}
        {exercise.instructions && exercise.instructions.length > 0 && (
          <Card className="border-0 shadow-lg mb-8">
            <CardContent className="p-6 md:p-8">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">
                Instructions
              </h2>
              <div className="space-y-4">
                {exercise.instructions.map((instruction, index) => (
                  <div 
                    key={index}
                    className="flex items-start gap-4"
                  >
                    <div className="w-8 h-8 bg-gradient-to-br from-sage-500 to-lavender-500 rounded-full flex items-center justify-center flex-shrink-0 text-white font-semibold text-sm">
                      {index + 1}
                    </div>
                    <p className="text-gray-700 pt-1">{instruction}</p>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        )}

        {/* Start Practice Button */}
        <div className="sticky bottom-6">
          <Button
            onClick={handleStartPractice}
            size="lg"
            className="w-full bg-gradient-to-r from-sage-500 to-lavender-500 text-white hover:opacity-90 rounded-full shadow-xl"
          >
            <Camera className="w-5 h-5 mr-2" />
            Start Practice with Camera
          </Button>
        </div>
      </div>
    </div>
  );
};

export default AsanaDetail;
