import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { exerciseService } from '@/services/exerciseService';
import type { PainCategory } from '@/types';
import { Card, CardContent } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';
import { toast } from 'sonner';
import { 
  User,
  Activity,
  Brain, 
  Heart,
  ArrowRight 
} from 'lucide-react';

const iconMap: { [key: string]: React.ElementType } = {
  neck_icon: User,
  back_icon: Activity,
  shoulder_icon: User,
  knee_icon: Activity,
  stress_icon: Brain,
  general_icon: Heart,
};

const PainSelector = () => {
  const [categories, setCategories] = useState<PainCategory[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    loadCategories();
  }, []);

  const loadCategories = async () => {
    try {
      const response = await exerciseService.getPainCategories();
      if (response.success) {
        setCategories(response.data);
      }
    } catch (error) {
      toast.error('Failed to load pain categories');
    } finally {
      setIsLoading(false);
    }
  };

  const handleSelect = (categoryName: string) => {
    const slug = categoryName.toLowerCase().replace(/\s+/g, '-');
    navigate(`/asanas/${slug}`);
  };

  if (isLoading) {
    return (
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        {[1, 2, 3, 4, 5, 6].map((i) => (
          <Skeleton key={i} className="h-48 rounded-2xl" />
        ))}
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
      {categories.map((category, index) => {
        const Icon = iconMap[category.icon] || Heart;
        return (
          <Card
            key={category.id}
            className="group cursor-pointer overflow-hidden border-0 shadow-lg hover:shadow-2xl transition-all duration-500 hover:-translate-y-2"
            onClick={() => handleSelect(category.name)}
            style={{
              animationDelay: `${index * 100}ms`,
            }}
          >
            <CardContent className="p-0">
              <div 
                className="h-48 relative overflow-hidden"
                style={{ backgroundColor: `${category.color}20` }}
              >
                {/* Background Pattern */}
                <div 
                  className="absolute inset-0 opacity-10"
                  style={{
                    backgroundImage: `radial-gradient(circle at 2px 2px, ${category.color} 1px, transparent 0)`,
                    backgroundSize: '20px 20px',
                  }}
                />
                
                {/* Content */}
                <div className="relative h-full flex flex-col items-center justify-center p-6">
                  <div 
                    className="w-16 h-16 rounded-2xl flex items-center justify-center mb-4 transform group-hover:scale-110 transition-transform duration-300"
                    style={{ backgroundColor: category.color }}
                  >
                    <Icon className="w-8 h-8 text-white" />
                  </div>
                  
                  <h3 className="text-xl font-semibold text-gray-900 text-center mb-2">
                    {category.name}
                  </h3>
                  
                  <p className="text-sm text-gray-600 text-center line-clamp-2">
                    {category.description}
                  </p>
                  
                  <div className="mt-4 flex items-center gap-2 text-sm font-medium" style={{ color: category.color }}>
                    <span>Explore Exercises</span>
                    <ArrowRight className="w-4 h-4 transform group-hover:translate-x-1 transition-transform" />
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        );
      })}
    </div>
  );
};

export default PainSelector;
