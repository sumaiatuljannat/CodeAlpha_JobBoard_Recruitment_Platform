import React, { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { Briefcase, Lock, Mail, ArrowRight, Sparkles, Shield, UserCheck } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import { useToast } from '../../context/ToastContext';

export const Login = () => {
  const { login, demoLogin } = useAuth();
  const { success, error } = useToast();
  const navigate = useNavigate();
  const location = useLocation();
  const from = location.state?.from?.pathname || '/';

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!email || !password) {
      error('Please enter both email and password.');
      return;
    }
    setSubmitting(true);
    try {
      const loggedUser = await login(email, password);
      success(`Welcome back, ${loggedUser.first_name || 'there'}!`);
      if (from !== '/') {
        navigate(from, { replace: true });
      } else if (loggedUser.role === 'employer') {
        navigate('/employer/dashboard');
      } else if (loggedUser.role === 'admin') {
        navigate('/admin/dashboard');
      } else {
        navigate('/candidate/dashboard');
      }
    } catch (err) {
      error(err.response?.data?.detail || err.response?.data?.non_field_errors?.[0] || 'Invalid email or password.');
    } finally {
      setSubmitting(false);
    }
  };

  const handleDemo = async (role) => {
    setSubmitting(true);
    try {
      const loggedUser = await demoLogin(role);
      success(`Logged in as demo ${role.toUpperCase()}`);
      if (role === 'employer') navigate('/employer/dashboard');
      else if (role === 'admin') navigate('/admin/dashboard');
      else navigate('/candidate/dashboard');
    } catch (err) {
      error('Demo login failed. Make sure backend is running.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="min-h-[80vh] flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8 bg-white p-8 rounded-3xl shadow-xl border border-slate-200">
        <div className="text-center">
          <div className="inline-flex p-3 rounded-2xl bg-brand-50 text-brand-600 mb-3">
            <Briefcase className="w-8 h-8" />
          </div>
          <h2 className="text-2xl font-bold text-slate-900 tracking-tight">Sign in to HireFlow</h2>
          <p className="text-xs text-slate-500 mt-1">Access your recruitment dashboard or candidate portal</p>
        </div>

        {/* Demo 1-Click Fast Logins */}
        <div className="bg-slate-50 border border-slate-200/80 rounded-2xl p-3.5 space-y-2">
          <div className="flex items-center gap-1.5 text-xs font-semibold text-slate-600">
            <Sparkles className="w-3.5 h-3.5 text-brand-600" />
            <span>1-Click Test Personas (Instant Login)</span>
          </div>
          <div className="grid grid-cols-3 gap-2">
            <button
              type="button"
              onClick={() => handleDemo('candidate')}
              disabled={submitting}
              className="px-2 py-2 rounded-xl bg-white border border-slate-200 hover:border-brand-500 hover:bg-brand-50 text-slate-700 text-xs font-medium flex flex-col items-center gap-1 transition-all shadow-sm"
            >
              <UserCheck className="w-4 h-4 text-emerald-600" />
              <span>Candidate</span>
            </button>
            <button
              type="button"
              onClick={() => handleDemo('employer')}
              disabled={submitting}
              className="px-2 py-2 rounded-xl bg-white border border-slate-200 hover:border-brand-500 hover:bg-brand-50 text-slate-700 text-xs font-medium flex flex-col items-center gap-1 transition-all shadow-sm"
            >
              <Briefcase className="w-4 h-4 text-brand-600" />
              <span>Recruiter</span>
            </button>
            <button
              type="button"
              onClick={() => handleDemo('admin')}
              disabled={submitting}
              className="px-2 py-2 rounded-xl bg-white border border-slate-200 hover:border-brand-500 hover:bg-brand-50 text-slate-700 text-xs font-medium flex flex-col items-center gap-1 transition-all shadow-sm"
            >
              <Shield className="w-4 h-4 text-purple-600" />
              <span>Admin</span>
            </button>
          </div>
        </div>

        <div className="relative">
          <div className="absolute inset-0 flex items-center"><div className="w-full border-t border-slate-200"></div></div>
          <div className="relative flex justify-center text-xs uppercase"><span className="bg-white px-2 text-slate-400 font-medium">Or with credentials</span></div>
        </div>

        {/* Credentials Form */}
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">Email Address</label>
            <div className="relative">
              <Mail className="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="name@example.com"
                required
                className="w-full pl-10 pr-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-brand-500/20 focus:border-brand-500 transition-all"
              />
            </div>
          </div>

          <div>
            <div className="flex items-center justify-between mb-1">
              <label className="block text-xs font-semibold text-slate-700">Password</label>
              <Link to="/forgot-password" className="text-xs text-brand-600 hover:underline">
                Forgot password?
              </Link>
            </div>
            <div className="relative">
              <Lock className="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                required
                className="w-full pl-10 pr-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-brand-500/20 focus:border-brand-500 transition-all"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={submitting}
            className="w-full py-2.5 rounded-xl bg-brand-600 text-white font-semibold text-sm hover:bg-brand-700 transition-colors shadow-md shadow-brand-500/25 flex items-center justify-center gap-2 disabled:opacity-60"
          >
            {submitting ? (
              <span className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
            ) : (
              <>
                <span>Sign In</span>
                <ArrowRight className="w-4 h-4" />
              </>
            )}
          </button>
        </form>

        <p className="text-center text-xs text-slate-500">
          Don't have an account?{' '}
          <Link to="/register" className="font-semibold text-brand-600 hover:underline">
            Register here
          </Link>
        </p>
      </div>
    </div>
  );
};
