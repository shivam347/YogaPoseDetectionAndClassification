import { useNavigate } from 'react-router-dom';
import type { Exercise } from '@/types';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Clock, TrendingUp, ArrowRight } from 'lucide-react';

interface AsanaCardProps {
  exercise: Exercise;
  index?: number;
}

const AsanaCard = ({ exercise, index = 0 }: AsanaCardProps) => {
  const navigate = useNavigate();

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
    if (seconds < 60) return `${seconds}s`;
    return `${Math.floor(seconds / 60)}m`;
  };

  return (
    <Card
      className="group cursor-pointer overflow-hidden border-0 shadow-lg hover:shadow-2xl transition-all duration-500 hover:-translate-y-2"
      onClick={() => navigate(`/asana/${exercise.id}`)}
      style={{
        animation: `fadeInUp 0.6s ease-out ${index * 100}ms both`,
      }}
    >
      <CardContent className="p-0">
        {/* Image */}
        <div className="relative h-48 overflow-hidden bg-gradient-to-br from-sage-100 to-lavender-100">
          {exercise.image_url ? (
            <img
              src={exercise.image_url}
              alt={exercise.name}
              className="w-full h-full object-cover transform group-hover:scale-110 transition-transform duration-700"
            />
          ) : (
            <div className="w-full h-full flex items-center justify-center">
              <div className="w-20 h-20 rounded-full bg-white/50 flex items-center justify-center">
                <span className="text-3xl font-serif text-sage-600">
                  {exercise.name.charAt(0)}
                </span>
              </div>
            </div>
          )}
          
          {/* Difficulty Badge */}
          <Badge 
            className={`absolute top-3 right-3 ${getDifficultyColor(exercise.difficulty_level)}`}
          >
            {exercise.difficulty_level}
          </Badge>
          
          {/* Overlay on hover */}
          <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
        </div>

        {/* Content */}
        <div className="p-5">
          <div className="mb-3">
            <h3 className="text-lg font-semibold text-gray-900 group-hover:text-sage-600 transition-colors">
              {exercise.name}
            </h3>
            {exercise.sanskrit_name && (
              <p className="text-sm text-gray-500 italic">
                {exercise.sanskrit_name}
              </p>
            )}
          </div>

          <p className="text-sm text-gray-600 line-clamp-2 mb-4">
            {exercise.description}
          </p>

          {/* Meta info */}
          <div className="flex items-center gap-4 text-sm text-gray-500">
            <div className="flex items-center gap-1">
              <Clock className="w-4 h-4" />
              <span>{formatDuration(exercise.duration_seconds)}</span>
            </div>
            {exercise.target_body_parts && exercise.target_body_parts.length > 0 && (
              <div className="flex items-center gap-1">
                <TrendingUp className="w-4 h-4" />
                <span>{exercise.target_body_parts.length} targets</span>
              </div>
            )}
          </div>

          {/* CTA */}
          <div className="mt-4 pt-4 border-t border-gray-100 flex items-center justify-between">
            <span className="text-sm font-medium text-sage-600">View Details</span>
            <ArrowRight className="w-4 h-4 text-sage-600 transform group-hover:translate-x-1 transition-transform" />
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default AsanaCard;
