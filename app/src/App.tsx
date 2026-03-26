import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { PoseProvider } from './context/PoseContext';
import { Toaster } from '@/components/ui/sonner';

// Layout
import Navbar from './components/layout/Navbar';
import Footer from './components/layout/Footer';

// Pages
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import PainSelection from './pages/PainSelection';
import AsanaList from './pages/AsanaList';
import AsanaDetail from './pages/AsanaDetail';
import AsanaPractice from './pages/AsanaPractice';
import Profile from './pages/Profile';

// Protected Route
import ProtectedRoute from './components/layout/ProtectedRoute';

function App() {
  return (
    <AuthProvider>
      <PoseProvider>
        <Router>
          <div className="min-h-screen bg-gradient-to-br from-sage-50 via-white to-lavender-50">
            <Navbar />
            <main className="flex-1">
              <Routes>
                {/* Public Routes */}
                <Route path="/" element={<Home />} />
                <Route path="/login" element={<Login />} />
                <Route path="/register" element={<Register />} />
                
                {/* Protected Routes */}
                <Route path="/dashboard" element={
                  <ProtectedRoute>
                    <Dashboard />
                  </ProtectedRoute>
                } />
                <Route path="/pain-selection" element={
                  <ProtectedRoute>
                    <PainSelection />
                  </ProtectedRoute>
                } />
                <Route path="/asanas/:painType" element={
                  <ProtectedRoute>
                    <AsanaList />
                  </ProtectedRoute>
                } />
                <Route path="/asana/:id" element={
                  <ProtectedRoute>
                    <AsanaDetail />
                  </ProtectedRoute>
                } />
                <Route path="/practice/:id" element={
                  <ProtectedRoute>
                    <AsanaPractice />
                  </ProtectedRoute>
                } />
                <Route path="/profile" element={
                  <ProtectedRoute>
                    <Profile />
                  </ProtectedRoute>
                } />
                
                {/* Fallback */}
                <Route path="*" element={<Navigate to="/" replace />} />
              </Routes>
            </main>
            <Footer />
            <Toaster position="top-right" richColors />
          </div>
        </Router>
      </PoseProvider>
    </AuthProvider>
  );
}

export default App;
