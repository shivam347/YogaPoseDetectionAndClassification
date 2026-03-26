import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '@/context/AuthContext';
import { practiceService } from '@/services/practiceService';
import type { PracticeStatistics, PracticeSession } from '@/types';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import { Skeleton } from '@/components/ui/skeleton';
import { 
  Activity, 
  Calendar, 
  TrendingUp, 
  Award, 
  Clock,
  Flame,
  ChevronRight,
  Play
} from 'lucide-react';
import { toast } from 'sonner';

const Dashboard = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [statistics, setStatistics] = useState<PracticeStatistics | null>(null);
  const [recentSessions, setRecentSessions] = useState<PracticeSession[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      const [statsResponse, historyResponse] = await Promise.all([
        practiceService.getStatistics(),
        practiceService.getPracticeHistory({ limit: 5 }),
      ]);

      if (statsResponse.success) {
        setStatistics(statsResponse.data);
      }

      if (historyResponse.success) {
        setRecentSessions(historyResponse.data.sessions);
      }
    } catch (error) {
      toast.error('Failed to load dashboard data');
    } finally {
      setIsLoading(false);
    }
  };

  const getGreeting = () => {
    const hour = new Date().getHours();
    if (hour < 12) return 'Good morning';
    if (hour < 18) return 'Good afternoon';
    return 'Good evening';
  };

  if (isLoading) {
    return (
      <div className="min-h-screen pt-24 pb-12 px-4">
        <div className="max-w-7xl mx-auto">
          <Skeleton className="h-32 rounded-2xl mb-8" />
          <div className="grid md:grid-cols-4 gap-6 mb-8">
            {[1, 2, 3, 4].map((i) => (
              <Skeleton key={i} className="h-32 rounded-2xl" />
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen pt-24 pb-12 px-4 bg-gradient-to-br from-sage-50 via-white to-lavender-50">
      <div className="max-w-7xl mx-auto">
        {/* Welcome Section */}
        <div className="mb-8">
          <h1 className="text-3xl md:text-4xl font-serif font-bold text-gray-900 mb-2">
            {getGreeting()}, {user?.name}!
          </h1>
          <p className="text-gray-600">
            Ready to continue your yoga journey? Let's practice together.
          </p>
        </div>

        {/* Quick Actions */}
        <Card className="mb-8 border-0 shadow-lg bg-gradient-to-r from-sage-500 to-lavender-500">
          <CardContent className="p-6">
            <div className="flex flex-col md:flex-row items-center justify-between gap-4">
              <div className="text-white">
                <h2 className="text-xl font-semibold mb-1">Start a New Practice</h2>
                <p className="text-white/80">Choose exercises based on your needs</p>
              </div>
              <Button 
                onClick={() => navigate('/pain-selection')}
                className="bg-white text-sage-600 hover:bg-gray-100 rounded-full px-6"
              >
                <Play className="w-4 h-4 mr-2" />
                Start Practice
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Statistics Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <Card className="border-0 shadow-lg">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-500 mb-1">Total Sessions</p>
                  <p className="text-3xl font-bold text-gray-900">
                    {statistics?.total_sessions || 0}
                  </p>
                </div>
                <div className="w-12 h-12 bg-sage-100 rounded-xl flex items-center justify-center">
                  <Activity className="w-6 h-6 text-sage-600" />
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="border-0 shadow-lg">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-500 mb-1">Practice Time</p>
                  <p className="text-3xl font-bold text-gray-900">
                    {statistics?.total_minutes || 0}m
                  </p>
                </div>
                <div className="w-12 h-12 bg-lavender-100 rounded-xl flex items-center justify-center">
                  <Clock className="w-6 h-6 text-lavender-600" />
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="border-0 shadow-lg">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-500 mb-1">Avg Accuracy</p>
                  <p className="text-3xl font-bold text-gray-900">
                    {statistics?.average_accuracy || 0}%
                  </p>
                </div>
                <div className="w-12 h-12 bg-yellow-100 rounded-xl flex items-center justify-center">
                  <TrendingUp className="w-6 h-6 text-yellow-600" />
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="border-0 shadow-lg">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-500 mb-1">Day Streak</p>
                  <p className="text-3xl font-bold text-gray-900">
                    {statistics?.streak_days || 0}
                  </p>
                </div>
                <div className="w-12 h-12 bg-orange-100 rounded-xl flex items-center justify-center">
                  <Flame className="w-6 h-6 text-orange-600" />
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Main Content Grid */}
        <div className="grid lg:grid-cols-3 gap-8">
          {/* Recent Sessions */}
          <div className="lg:col-span-2">
            <Card className="border-0 shadow-lg">
              <CardHeader className="flex flex-row items-center justify-between">
                <CardTitle className="text-xl font-semibold">Recent Sessions</CardTitle>
                <Button 
                  variant="ghost" 
                  size="sm"
                  onClick={() => navigate('/practice-history')}
                >
                  View All
                  <ChevronRight className="w-4 h-4 ml-1" />
                </Button>
              </CardHeader>
              <CardContent>
                {recentSessions.length === 0 ? (
                  <div className="text-center py-12">
                    <Calendar className="w-12 h-12 text-gray-300 mx-auto mb-4" />
                    <p className="text-gray-500 mb-4">No practice sessions yet</p>
                    <Button 
                      onClick={() => navigate('/pain-selection')}
                      variant="outline"
                    >
                      Start Your First Session
                    </Button>
                  </div>
                ) : (
                  <div className="space-y-4">
                    {recentSessions.map((session) => (
                      <div 
                        key={session.id}
                        className="flex items-center justify-between p-4 bg-gray-50 rounded-xl hover:bg-gray-100 transition-colors"
                      >
                        <div className="flex items-center gap-4">
                          <div className="w-10 h-10 bg-sage-100 rounded-lg flex items-center justify-center">
                            <Award className="w-5 h-5 text-sage-600" />
                          </div>
                          <div>
                            <p className="font-medium text-gray-900">
                              {session.exercise_name}
                            </p>
                            <p className="text-sm text-gray-500">
                              {new Date(session.practiced_at).toLocaleDateString()}
                            </p>
                          </div>
                        </div>
                        <div className="text-right">
                          <p className="font-semibold text-sage-600">
                            {session.accuracy_percentage}%
                          </p>
                          <p className="text-sm text-gray-500">
                            {session.duration_seconds}s
                          </p>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>
          </div>

          {/* Progress & Goals */}
          <div>
            <Card className="border-0 shadow-lg mb-6">
              <CardHeader>
                <CardTitle className="text-xl font-semibold">Your Progress</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-6">
                  <div>
                    <div className="flex justify-between mb-2">
                      <span className="text-sm text-gray-600">Accuracy Goal (80%)</span>
                      <span className="text-sm font-medium text-gray-900">
                        {statistics?.average_accuracy || 0}%
                      </span>
                    </div>
                    <Progress 
                      value={Math.min((statistics?.average_accuracy || 0) / 80 * 100, 100)} 
                      className="h-2"
                    />
                  </div>
                  
                  <div>
                    <div className="flex justify-between mb-2">
                      <span className="text-sm text-gray-600">Sessions Goal (30)</span>
                      <span className="text-sm font-medium text-gray-900">
                        {statistics?.total_sessions || 0}
                      </span>
                    </div>
                    <Progress 
                      value={Math.min((statistics?.total_sessions || 0) / 30 * 100, 100)} 
                      className="h-2"
                    />
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Top Exercises */}
            {statistics?.top_exercises && statistics.top_exercises.length > 0 && (
              <Card className="border-0 shadow-lg">
                <CardHeader>
                  <CardTitle className="text-xl font-semibold">Top Exercises</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    {statistics.top_exercises.slice(0, 3).map((exercise, index) => (
                      <div 
                        key={exercise.name}
                        className="flex items-center justify-between"
                      >
                        <div className="flex items-center gap-3">
                          <span className="w-6 h-6 bg-sage-100 rounded-full flex items-center justify-center text-sm font-medium text-sage-600">
                            {index + 1}
                          </span>
                          <span className="text-gray-700">{exercise.name}</span>
                        </div>
                        <span className="text-sm text-gray-500">
                          {exercise.count} times
                        </span>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
