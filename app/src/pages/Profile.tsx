import { useEffect, useState } from 'react';
import { useAuth } from '@/context/AuthContext';
import { authService } from '@/services/authService';
import type { User } from '@/types';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Skeleton } from '@/components/ui/skeleton';
import { 
  User as UserIcon, 
  Mail, 
  Calendar, 
  Activity,
  Edit2,
  Save,
  X
} from 'lucide-react';
import { toast } from 'sonner';

const Profile = () => {
  const { updateUser } = useAuth();
  const [user, setUser] = useState<User & { total_sessions?: number; average_accuracy?: number } | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isEditing, setIsEditing] = useState(false);
  const [editName, setEditName] = useState('');

  useEffect(() => {
    loadProfile();
  }, []);

  const loadProfile = async () => {
    try {
      setIsLoading(true);
      const response = await authService.getProfile();
      if (response.success) {
        setUser(response.data);
        setEditName(response.data.name);
      }
    } catch (error) {
      toast.error('Failed to load profile');
    } finally {
      setIsLoading(false);
    }
  };

  const handleSave = async () => {
    if (!editName.trim()) {
      toast.error('Name cannot be empty');
      return;
    }

    try {
      await updateUser({ name: editName });
      setUser(prev => prev ? { ...prev, name: editName } : null);
      setIsEditing(false);
    } catch (error) {
      toast.error('Failed to update profile');
    }
  };

  const handleCancel = () => {
    setEditName(user?.name || '');
    setIsEditing(false);
  };

  if (isLoading) {
    return (
      <div className="min-h-screen pt-24 pb-12 px-4">
        <div className="max-w-2xl mx-auto">
          <Skeleton className="h-64 rounded-2xl" />
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen pt-24 pb-12 px-4 bg-gradient-to-br from-sage-50 via-white to-lavender-50">
      <div className="max-w-2xl mx-auto">
        <h1 className="text-3xl font-serif font-bold text-gray-900 mb-8">
          Your Profile
        </h1>

        {/* Profile Card */}
        <Card className="border-0 shadow-xl mb-8">
          <CardContent className="p-8">
            <div className="flex flex-col items-center">
              {/* Avatar */}
              <div className="w-24 h-24 bg-gradient-to-br from-sage-400 to-lavender-500 rounded-full flex items-center justify-center text-white text-3xl font-bold mb-6">
                {user?.name?.charAt(0).toUpperCase()}
              </div>

              {/* Name */}
              {isEditing ? (
                <div className="w-full max-w-sm mb-4">
                  <Label htmlFor="name">Name</Label>
                  <div className="flex gap-2 mt-1">
                    <Input
                      id="name"
                      value={editName}
                      onChange={(e) => setEditName(e.target.value)}
                      className="flex-1"
                    />
                    <Button onClick={handleSave} size="icon" className="bg-sage-500">
                      <Save className="w-4 h-4" />
                    </Button>
                    <Button onClick={handleCancel} size="icon" variant="outline">
                      <X className="w-4 h-4" />
                    </Button>
                  </div>
                </div>
              ) : (
                <div className="flex items-center gap-2 mb-2">
                  <h2 className="text-2xl font-semibold text-gray-900">
                    {user?.name}
                  </h2>
                  <Button 
                    variant="ghost" 
                    size="icon"
                    onClick={() => setIsEditing(true)}
                  >
                    <Edit2 className="w-4 h-4 text-gray-400" />
                  </Button>
                </div>
              )}

              <p className="text-gray-500">{user?.email}</p>
            </div>
          </CardContent>
        </Card>

        {/* Stats Grid */}
        <div className="grid sm:grid-cols-2 gap-4 mb-8">
          <Card className="border-0 shadow-lg">
            <CardContent className="p-6">
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 bg-sage-100 rounded-xl flex items-center justify-center">
                  <Activity className="w-6 h-6 text-sage-600" />
                </div>
                <div>
                  <p className="text-sm text-gray-500">Total Sessions</p>
                  <p className="text-2xl font-bold text-gray-900">
                    {user?.total_sessions || 0}
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="border-0 shadow-lg">
            <CardContent className="p-6">
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 bg-lavender-100 rounded-xl flex items-center justify-center">
                  <Activity className="w-6 h-6 text-lavender-600" />
                </div>
                <div>
                  <p className="text-sm text-gray-500">Average Accuracy</p>
                  <p className="text-2xl font-bold text-gray-900">
                    {user?.average_accuracy || 0}%
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Account Info */}
        <Card className="border-0 shadow-lg">
          <CardHeader>
            <CardTitle className="text-lg">Account Information</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center gap-4 p-4 bg-gray-50 rounded-xl">
              <UserIcon className="w-5 h-5 text-gray-400" />
              <div>
                <p className="text-sm text-gray-500">Full Name</p>
                <p className="font-medium">{user?.name}</p>
              </div>
            </div>

            <div className="flex items-center gap-4 p-4 bg-gray-50 rounded-xl">
              <Mail className="w-5 h-5 text-gray-400" />
              <div>
                <p className="text-sm text-gray-500">Email Address</p>
                <p className="font-medium">{user?.email}</p>
              </div>
            </div>

            <div className="flex items-center gap-4 p-4 bg-gray-50 rounded-xl">
              <Calendar className="w-5 h-5 text-gray-400" />
              <div>
                <p className="text-sm text-gray-500">Member Since</p>
                <p className="font-medium">
                  {user?.created_at 
                    ? new Date(user.created_at).toLocaleDateString() 
                    : 'N/A'}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Profile;
