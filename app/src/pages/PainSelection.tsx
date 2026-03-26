import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '@/context/AuthContext';
import PainSelector from '@/components/exercise/PainSelector';
import { Card, CardContent } from '@/components/ui/card';
import { ArrowLeft, Sparkles } from 'lucide-react';
import { Button } from '@/components/ui/button';

const PainSelection = () => {
  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login');
    }
  }, [isAuthenticated, navigate]);

  return (
    <div className="min-h-screen pt-24 pb-12 px-4 bg-gradient-to-br from-sage-50 via-white to-lavender-50">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <Button 
            variant="ghost" 
            className="mb-4"
            onClick={() => navigate('/dashboard')}
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Dashboard
          </Button>
          
          <div className="flex items-center gap-3 mb-4">
            <div className="w-12 h-12 bg-gradient-to-br from-sage-400 to-lavender-500 rounded-xl flex items-center justify-center">
              <Sparkles className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-3xl font-serif font-bold text-gray-900">
                What would you like to work on?
              </h1>
              <p className="text-gray-600">
                Select an area to find exercises tailored to your needs
              </p>
            </div>
          </div>
        </div>

        {/* Info Card */}
        <Card className="mb-8 border-0 shadow-lg bg-gradient-to-r from-sage-50 to-lavender-50">
          <CardContent className="p-6">
            <div className="flex items-start gap-4">
              <div className="w-10 h-10 bg-white rounded-lg flex items-center justify-center shadow-sm">
                <span className="text-xl">💡</span>
              </div>
              <div>
                <h3 className="font-semibold text-gray-900 mb-1">
                  How it works
                </h3>
                <p className="text-gray-600 text-sm">
                  Choose the area where you're experiencing discomfort or want to improve. 
                  Our AI will recommend specific yoga poses and exercises designed to help 
                  with that particular concern. Each exercise includes detailed instructions 
                  and real-time feedback when you practice.
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Pain Categories */}
        <PainSelector />
      </div>
    </div>
  );
};

export default PainSelection;
