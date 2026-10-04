import React, { createContext, useContext, useState, useEffect } from 'react';
import api from '../api/client';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('hireflow_token'));
  const [loading, setLoading] = useState(true);

  // Fetch current user details on load if token exists
  useEffect(() => {
    const fetchMe = async () => {
      const storedToken = localStorage.getItem('hireflow_token');
      if (!storedToken) {
        setLoading(false);
        return;
      }
      try {
        const res = await api.get('/api/auth/me/');
        if (res.data?.user) {
          setUser(res.data.user);
          localStorage.setItem('hireflow_user', JSON.stringify(res.data.user));
        }
      } catch (err) {
        console.error('Failed to authenticate token:', err);
        localStorage.removeItem('hireflow_token');
        localStorage.removeItem('hireflow_refresh');
        localStorage.removeItem('hireflow_user');
        setUser(null);
        setToken(null);
      } finally {
        setLoading(false);
      }
    };

    fetchMe();
  }, []);

  const login = async (email, password) => {
    const res = await api.post('/api/auth/login/', { email, password });
    if (res.data?.access) {
      localStorage.setItem('hireflow_token', res.data.access);
      localStorage.setItem('hireflow_refresh', res.data.refresh);
      localStorage.setItem('hireflow_user', JSON.stringify(res.data.user));
      setToken(res.data.access);
      setUser(res.data.user);
      return res.data.user;
    }
  };

  const demoLogin = async (role) => {
    const res = await api.post('/api/auth/demo-login/', { role });
    if (res.data?.access) {
      localStorage.setItem('hireflow_token', res.data.access);
      localStorage.setItem('hireflow_refresh', res.data.refresh);
      localStorage.setItem('hireflow_user', JSON.stringify(res.data.user));
      setToken(res.data.access);
      setUser(res.data.user);
      return res.data.user;
    }
  };

  const register = async (userData) => {
    const res = await api.post('/api/auth/register/', userData);
    if (res.data?.access) {
      localStorage.setItem('hireflow_token', res.data.access);
      localStorage.setItem('hireflow_refresh', res.data.refresh);
      localStorage.setItem('hireflow_user', JSON.stringify(res.data.user));
      setToken(res.data.access);
      setUser(res.data.user);
      return res.data.user;
    }
  };

  const logout = async () => {
    const refresh = localStorage.getItem('hireflow_refresh');
    try {
      if (refresh) {
        await api.post('/api/auth/logout/', { refresh });
      }
    } catch (e) {
      // Ignore
    } finally {
      localStorage.removeItem('hireflow_token');
      localStorage.removeItem('hireflow_refresh');
      localStorage.removeItem('hireflow_user');
      setUser(null);
      setToken(null);
    }
  };

  const updateUser = (updated) => {
    setUser((prev) => {
      const neu = { ...prev, ...updated };
      localStorage.setItem('hireflow_user', JSON.stringify(neu));
      return neu;
    });
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        loading,
        isAuthenticated: !!user,
        role: user?.role,
        isCandidate: user?.role === 'candidate',
        isEmployer: user?.role === 'employer',
        isAdmin: user?.role === 'admin' || user?.is_staff,
        login,
        demoLogin,
        register,
        logout,
        updateUser,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
