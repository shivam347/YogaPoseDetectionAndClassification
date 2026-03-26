import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { exerciseService } from '@/services/exerciseService';
import type { Exercise } from '@/types';
import AsanaCard from '@/components/exercise/AsanaCard';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Skeleton } from '@/components/ui/skeleton';
import { ArrowLeft, Search, Filter, Sparkles } from 'lucide-react';
import { toast } from 'sonner';

const AsanaList = () => {
  const { painType } = useParams<{ painType: string }>();
  const navigate = useNavigate();
  const [exercises, setExercises] = useState<Exercise[]>([]);
  const [filteredExercises, setFilteredExercises] = useState<Exercise[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedDifficulty, setSelectedDifficulty] = useState<string>('all');

  useEffect(() => {
    loadExercises();
  }, [painType]);

  useEffect(() => {
    filterExercises();
  }, [searchQuery, selectedDifficulty, exercises]);

  const loadExercises = async () => {
    try {
      setIsLoading(true);
      const painTypeFormatted = painType?.replace(/-/g, ' ');
      const response = await exerciseService.getExercises({ 
        pain_type: painTypeFormatted 
      });
      
      if (response.success) {
        setExercises(response.data);
        setFilteredExercises(response.data);
      }
    } catch (error) {
      toast.error('Failed to load exercises');
    } finally {
      setIsLoading(false);
    }
  };

  const filterExercises = () => {
    let filtered = exercises;

    if (searchQuery) {
      filtered = filtered.filter(ex =>
        ex.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        ex.sanskrit_name?.toLowerCase().includes(searchQuery.toLowerCase()) ||
        ex.description.toLowerCase().includes(searchQuery.toLowerCase())
      );
    }

    if (selectedDifficulty !== 'all') {
      filtered = filtered.filter(ex => ex.difficulty_level === selectedDifficulty);
    }

    setFilteredExercises(filtered);
  };

  const getPainTypeDisplay = () => {
    if (!painType) return 'Exercises';
    return painType.split('-').map(word => 
      word.charAt(0).toUpperCase() + word.slice(1)
    ).join(' ');
  };

  if (isLoading) {
    return (
      <div className="min-h-screen pt-24 pb-12 px-4">
        <div className="max-w-6xl mx-auto">
          <Skeleton className="h-12 w-64 mb-8" />
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[1, 2, 3, 4, 5, 6].map((i) => (
              <Skeleton key={i} className="h-80 rounded-2xl" />
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen pt-24 pb-12 px-4 bg-gradient-to-br from-sage-50 via-white to-lavender-50">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <Button 
            variant="ghost" 
            className="mb-4"
            onClick={() => navigate('/pain-selection')}
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Categories
          </Button>
          
          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 bg-gradient-to-br from-sage-400 to-lavender-500 rounded-xl flex items-center justify-center">
                <Sparkles className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-3xl font-serif font-bold text-gray-900">
                  {getPainTypeDisplay()}
                </h1>
                <p className="text-gray-600">
                  {exercises.length} exercises available
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Filters */}
        <div className="flex flex-col sm:flex-row gap-4 mb-8">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
            <Input
              placeholder="Search exercises..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-10"
            />
          </div>
          
          <div className="flex gap-2">
            <Button
              variant={selectedDifficulty === 'all' ? 'default' : 'outline'}
              onClick={() => setSelectedDifficulty('all')}
              className={selectedDifficulty === 'all' ? 'bg-sage-500' : ''}
            >
              All
            </Button>
            <Button
              variant={selectedDifficulty === 'beginner' ? 'default' : 'outline'}
              onClick={() => setSelectedDifficulty('beginner')}
              className={selectedDifficulty === 'beginner' ? 'bg-green-500' : ''}
            >
              Beginner
            </Button>
            <Button
              variant={selectedDifficulty === 'intermediate' ? 'default' : 'outline'}
              onClick={() => setSelectedDifficulty('intermediate')}
              className={selectedDifficulty === 'intermediate' ? 'bg-yellow-500' : ''}
            >
              Intermediate
            </Button>
          </div>
        </div>

        {/* Results */}
        {filteredExercises.length === 0 ? (
          <div className="text-center py-16">
            <Filter className="w-16 h-16 text-gray-300 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-gray-700 mb-2">
              No exercises found
            </h3>
            <p className="text-gray-500 mb-4">
              Try adjusting your search or filters
            </p>
            <Button 
              variant="outline"
              onClick={() => {
                setSearchQuery('');
                setSelectedDifficulty('all');
              }}
            >
              Clear Filters
            </Button>
          </div>
        ) : (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredExercises.map((exercise, index) => (
              <AsanaCard 
                key={exercise.id} 
                exercise={exercise} 
                index={index}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default AsanaList;
