import { useEffect, useRef } from 'react';
import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { 
  Sparkles, 
  Camera, 
  Brain, 
  Activity, 
  ChevronRight,
  Star,
  Quote
} from 'lucide-react';

const Home = () => {
  const heroRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Simple scroll animation
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('animate-in');
          }
        });
      },
      { threshold: 0.1, rootMargin: '0px 0px -50px 0px' }
    );

    document.querySelectorAll('.animate-on-scroll').forEach((el) => {
      observer.observe(el);
    });

    return () => observer.disconnect();
  }, []);

  const features = [
    {
      icon: Camera,
      title: 'Real-time Detection',
      description: 'AI-powered pose detection using your camera for instant feedback.',
    },
    {
      icon: Brain,
      title: 'Smart Classification',
      description: 'Advanced ML algorithms identify poses with 90%+ accuracy.',
    },
    {
      icon: Activity,
      title: 'Progress Tracking',
      description: 'Monitor your improvement with detailed analytics and insights.',
    },
  ];

  const howItWorks = [
    {
      step: 1,
      title: 'Select Your Focus',
      description: 'Choose exercises based on your pain points or wellness goals.',
    },
    {
      step: 2,
      title: 'Follow the Guide',
      description: 'View detailed instructions and benefits for each pose.',
    },
    {
      step: 3,
      title: 'Practice with AI',
      description: 'Use your camera to get real-time feedback on your form.',
    },
  ];

  const testimonials = [
    {
      name: 'Sarah M.',
      role: 'Yoga Enthusiast',
      content: 'This app transformed my yoga practice! The real-time feedback helps me maintain proper form.',
      rating: 5,
    },
    {
      name: 'John D.',
      role: 'Fitness Beginner',
      content: 'As a beginner, I was worried about doing poses incorrectly. This app gives me confidence.',
      rating: 5,
    },
    {
      name: 'Emma L.',
      role: 'Physical Therapy Patient',
      content: 'The pain-specific exercises have helped my recovery tremendously. Highly recommended!',
      rating: 5,
    },
  ];

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section 
        ref={heroRef}
        className="relative min-h-screen flex items-center pt-20 overflow-hidden"
      >
        {/* Background Gradient */}
        <div className="absolute inset-0 bg-gradient-to-br from-sage-50 via-white to-lavender-50" />
        
        {/* Decorative Elements */}
        <div className="absolute top-20 right-10 w-72 h-72 bg-sage-200/30 rounded-full blur-3xl" />
        <div className="absolute bottom-20 left-10 w-96 h-96 bg-lavender-200/30 rounded-full blur-3xl" />
        
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            {/* Content */}
            <div className="space-y-8">
              <div className="inline-flex items-center gap-2 px-4 py-2 bg-sage-100 rounded-full text-sage-700 text-sm font-medium">
                <Sparkles className="w-4 h-4" />
                <span>AI-Powered Yoga Assistant</span>
              </div>
              
              <h1 className="text-5xl md:text-6xl lg:text-7xl font-serif font-bold text-gray-900 leading-tight">
                Discover Your
                <span className="block text-transparent bg-clip-text bg-gradient-to-r from-sage-500 to-lavender-500">
                  Perfect Pose
                </span>
              </h1>
              
              <p className="text-xl text-gray-600 max-w-lg">
                Experience the future of yoga with AI-powered pose detection and personalized guidance for a healthier, more balanced life.
              </p>
              
              <div className="flex flex-wrap gap-4">
                <Link to="/register">
                  <Button 
                    size="lg" 
                    className="bg-gradient-to-r from-sage-500 to-lavender-500 text-white hover:opacity-90 rounded-full px-8"
                  >
                    Start Your Journey
                    <ChevronRight className="w-5 h-5 ml-2" />
                  </Button>
                </Link>
                <Link to="/login">
                  <Button 
                    size="lg" 
                    variant="outline"
                    className="rounded-full px-8 border-2"
                  >
                    Sign In
                  </Button>
                </Link>
              </div>
              
              {/* Stats */}
              <div className="flex gap-8 pt-4">
                <div>
                  <p className="text-3xl font-bold text-gray-900">20+</p>
                  <p className="text-sm text-gray-500">Yoga Poses</p>
                </div>
                <div>
                  <p className="text-3xl font-bold text-gray-900">90%</p>
                  <p className="text-sm text-gray-500">Accuracy</p>
                </div>
                <div>
                  <p className="text-3xl font-bold text-gray-900">24/7</p>
                  <p className="text-sm text-gray-500">AI Guidance</p>
                </div>
              </div>
            </div>
            
            {/* Hero Image */}
            <div className="relative hidden lg:block">
              <div className="relative w-full aspect-square max-w-lg mx-auto">
                {/* Main Image Container */}
                <div className="absolute inset-0 rounded-3xl overflow-hidden shadow-2xl">
                  <img
                    src="https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=800&h=800&fit=crop"
                    alt="Yoga Practice"
                    className="w-full h-full object-cover"
                  />
                </div>
                
                {/* Floating Cards */}
                <div className="absolute -bottom-6 -left-6 bg-white rounded-2xl shadow-xl p-4 animate-bounce">
                  <div className="flex items-center gap-3">
                    <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center">
                      <Activity className="w-6 h-6 text-green-600" />
                    </div>
                    <div>
                      <p className="text-sm font-semibold text-gray-900">Pose Detected</p>
                      <p className="text-xs text-gray-500">Tree Pose - 95%</p>
                    </div>
                  </div>
                </div>
                
                <div className="absolute -top-6 -right-6 bg-white rounded-2xl shadow-xl p-4">
                  <div className="flex items-center gap-2">
                    <Star className="w-5 h-5 text-yellow-500 fill-yellow-500" />
                    <span className="text-sm font-semibold">4.9 Rating</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-24 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16 animate-on-scroll opacity-0 translate-y-8 transition-all duration-700">
            <h2 className="text-3xl md:text-4xl font-serif font-bold text-gray-900 mb-4">
              Key Features
            </h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Our AI-powered platform provides everything you need for a successful yoga practice.
            </p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <Card 
                key={feature.title}
                className="group border-0 shadow-lg hover:shadow-2xl transition-all duration-500 animate-on-scroll opacity-0 translate-y-8"
                style={{ transitionDelay: `${index * 100}ms` }}
              >
                <CardContent className="p-8">
                  <div className="w-14 h-14 bg-gradient-to-br from-sage-100 to-lavender-100 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
                    <feature.icon className="w-7 h-7 text-sage-600" />
                  </div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-3">
                    {feature.title}
                  </h3>
                  <p className="text-gray-600">
                    {feature.description}
                  </p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="py-24 bg-gradient-to-br from-sage-50 to-lavender-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16 animate-on-scroll opacity-0 translate-y-8 transition-all duration-700">
            <h2 className="text-3xl md:text-4xl font-serif font-bold text-gray-900 mb-4">
              How It Works
            </h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Get started with your AI-powered yoga journey in three simple steps.
            </p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8">
            {howItWorks.map((step, index) => (
              <div 
                key={step.step}
                className="relative animate-on-scroll opacity-0 translate-y-8 transition-all duration-700"
                style={{ transitionDelay: `${index * 150}ms` }}
              >
                <div className="bg-white rounded-3xl p-8 shadow-lg h-full">
                  <div className="w-12 h-12 bg-gradient-to-br from-sage-500 to-lavender-500 rounded-full flex items-center justify-center text-white font-bold text-lg mb-6">
                    {step.step}
                  </div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-3">
                    {step.title}
                  </h3>
                  <p className="text-gray-600">
                    {step.description}
                  </p>
                </div>
                
                {index < howItWorks.length - 1 && (
                  <div className="hidden md:block absolute top-1/2 -right-4 transform -translate-y-1/2 z-10">
                    <ChevronRight className="w-8 h-8 text-sage-300" />
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section className="py-24 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16 animate-on-scroll opacity-0 translate-y-8 transition-all duration-700">
            <h2 className="text-3xl md:text-4xl font-serif font-bold text-gray-900 mb-4">
              What Our Users Say
            </h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Join thousands of satisfied users who have transformed their yoga practice.
            </p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8">
            {testimonials.map((testimonial, index) => (
              <Card 
                key={testimonial.name}
                className="border-0 shadow-lg animate-on-scroll opacity-0 translate-y-8"
                style={{ transitionDelay: `${index * 100}ms` }}
              >
                <CardContent className="p-8">
                  <Quote className="w-10 h-10 text-sage-200 mb-4" />
                  
                  <div className="flex gap-1 mb-4">
                    {[...Array(testimonial.rating)].map((_, i) => (
                      <Star key={i} className="w-5 h-5 text-yellow-500 fill-yellow-500" />
                    ))}
                  </div>
                  
                  <p className="text-gray-700 mb-6">
                    "{testimonial.content}"
                  </p>
                  
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 bg-gradient-to-br from-sage-400 to-lavender-500 rounded-full flex items-center justify-center text-white font-semibold">
                      {testimonial.name.charAt(0)}
                    </div>
                    <div>
                      <p className="font-semibold text-gray-900">{testimonial.name}</p>
                      <p className="text-sm text-gray-500">{testimonial.role}</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-24 bg-gradient-to-br from-sage-500 to-lavender-500">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl md:text-4xl font-serif font-bold text-white mb-6">
            Ready to Start Your Yoga Journey?
          </h2>
          <p className="text-xl text-white/90 mb-8 max-w-2xl mx-auto">
            Join thousands of users who have transformed their practice with AI-powered guidance.
          </p>
          <div className="flex flex-wrap justify-center gap-4">
            <Link to="/register">
              <Button 
                size="lg" 
                className="bg-white text-sage-600 hover:bg-gray-100 rounded-full px-8"
              >
                Get Started Free
              </Button>
            </Link>
            <Link to="/login">
              <Button 
                size="lg" 
                variant="outline"
                className="border-2 border-white text-white hover:bg-white/10 rounded-full px-8"
              >
                Sign In
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Add animation styles */}
      <style>{`
        .animate-in {
          opacity: 1 !important;
          transform: translateY(0) !important;
        }
      `}</style>
    </div>
  );
};

export default Home;
