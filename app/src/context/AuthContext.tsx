import React, { createContext, useContext, useState, useEffect, type ReactNode } from 'react';
import { authService } from '@/services/authService';
import type { User } from '@/types';
import { toast } from 'sonner';

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<boolean>;
  register: (name: string, email: string, password: string) => Promise<boolean>;
  logout: () => void;
  updateUser: (data: Partial<User>) => Promise<void>;
  refreshUser: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const initAuth = async () => {
      const token = authService.getToken();
      if (token) {
        try {
          await refreshUser();
        } catch (error) {
          authService.logout();
        }
      }
      setIsLoading(false);
    };

    initAuth();
  }, []);

  const login = async (email: string, password: string): Promise<boolean> => {
    try {
      setIsLoading(true);
      const response = await authService.login(email, password);
      
      if (response.success) {
        authService.setAuthData(response.data.token, response.data);
        setUser({
          id: response.data.user_id,
          name: response.data.name,
          email: response.data.email,
        });
        toast.success('Login successful!');
        return true;
      }
      return false;
    } catch (error: any) {
      toast.error(error.response?.data?.message || 'Login failed');
      return false;
    } finally {
      setIsLoading(false);
    }
  };

  const register = async (name: string, email: string, password: string): Promise<boolean> => {
    try {
      setIsLoading(true);
      const response = await authService.register(name, email, password);
      
      if (response.success) {
        authService.setAuthData(response.data.token, response.data);
        setUser({
          id: response.data.user_id,
          name: response.data.name,
          email: response.data.email,
        });
        toast.success('Registration successful!');
        return true;
      }
      return false;
    } catch (error: any) {
      toast.error(error.response?.data?.message || 'Registration failed');
      return false;
    } finally {
      setIsLoading(false);
    }
  };

  const logout = () => {
    authService.logout();
    setUser(null);
    toast.info('Logged out successfully');
  };

  const updateUser = async (data: Partial<User>) => {
    try {
      const response = await authService.updateProfile(data);
      if (response.success) {
        setUser(prev => prev ? { ...prev, ...data } : null);
        toast.success('Profile updated');
      }
    } catch (error) {
      toast.error('Failed to update profile');
    }
  };

  const refreshUser = async () => {
    try {
      const response = await authService.getProfile();
      if (response.success) {
        setUser(response.data);
      }
    } catch (error) {
      throw error;
    }
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        isAuthenticated: !!user,
        isLoading,
        login,
        register,
        logout,
        updateUser,
        refreshUser,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
