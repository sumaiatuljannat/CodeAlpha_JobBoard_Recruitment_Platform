import React, { useState, useEffect, useRef } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import {
  Briefcase,
  Bell,
  User as UserIcon,
  LogOut,
  ChevronDown,
  Menu,
  X,
  Sparkles,
  ShieldCheck,
  Building2,
  Bookmark,
  FileText,
  Users,
  CreditCard,
  Layers,
  Search,
  Moon,
  Sun,
} from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import { useToast } from '../../context/ToastContext';
import api from '../../api/client';

export const Navbar = () => {
  const { user, isAuthenticated, role, logout, demoLogin } = useAuth();
  const { success, info } = useToast();
  const navigate = useNavigate();
  const location = useLocation();

  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [profileDropdownOpen, setProfileDropdownOpen] = useState(false);
  const [notifDropdownOpen, setNotifDropdownOpen] = useState(false);
  const [notifications, setNotifications] = useState([]);
  const [unreadCount, setUnreadCount] = useState(0);
  const [isDark, setIsDark] = useState(() => localStorage.getItem('hireflow_theme') === 'dark');

  const profileRef = useRef(null);
  const notifRef = useRef(null);

  // Fetch notifications if authenticated
  const fetchNotifications = async () => {
    if (!isAuthenticated) return;
    try {
      const res = await api.get('/api/notifications/');
      const list = res.data?.results || res.data || [];
      setNotifications(list.slice(0, 8));
      const unread = list.filter((n) => !n.is_read).length;
      setUnreadCount(unread);
    } catch (e) {
      // Ignore
    }
  };

  useEffect(() => {
    fetchNotifications();
    const interval = setInterval(fetchNotifications, 30000);
    return () => clearInterval(interval);
  }, [isAuthenticated]);

  // Click outside listener for dropdowns
  useEffect(() => {
    const handleClickOutside = (e) => {
      if (profileRef.current && !profileRef.current.contains(e.target)) {
        setProfileDropdownOpen(false);
      }
      if (notifRef.current && !notifRef.current.contains(e.target)) {
        setNotifDropdownOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  // Close menus on route change
  useEffect(() => {
    setMobileMenuOpen(false);
    setProfileDropdownOpen(false);
    setNotifDropdownOpen(false);
  }, [location.pathname]);

  const handleDemoSwitch = async (targetRole) => {
    try {
      await demoLogin(targetRole);
      success(`Switched active persona to ${targetRole.toUpperCase()}`);
      if (targetRole === 'employer') navigate('/employer/dashboard');
      else if (targetRole === 'admin') navigate('/admin/dashboard');
      else navigate('/candidate/dashboard');
    } catch (err) {
      console.error(err);
    }
  };

  const handleMarkAllRead = async () => {
    try {
      await api.post('/api/notifications/read_all/');
      setUnreadCount(0);
      setNotifications((prev) => prev.map((n) => ({ ...n, is_read: true })));
      info('All notifications marked as read.');
    } catch (e) {
      //
    }
  };

  const handleLogout = async () => {
    await logout();
    info('You have logged out.');
    navigate('/');
  };

  const handleThemeToggle = () => {
    const nextIsDark = !isDark;
    setIsDark(nextIsDark);
    document.documentElement.classList.toggle('dark', nextIsDark);
    localStorage.setItem('hireflow_theme', nextIsDark ? 'dark' : 'light');
  };

  return (
    <header className="sticky top-0 z-40 bg-white/95 backdrop-blur-md border-b border-slate-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <div className="flex items-center gap-8">
            <Link to="/" className="flex items-center gap-2.5 group">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-brand-700 via-brand-600 to-indigo-500 flex items-center justify-center text-white shadow-md shadow-brand-500/20 group-hover:scale-105 transition-transform">
                <Briefcase className="w-5 h-5" />
              </div>
              <div>
                <span className="theme-wordmark text-xl font-bold bg-gradient-to-r from-slate-900 via-brand-900 to-brand-700 bg-clip-text text-transparent">
                  HireFlow
                </span>
                <span className="hidden sm:inline-block ml-1.5 px-1.5 py-0.2 rounded text-[10px] font-semibold bg-brand-50 text-brand-700 border border-brand-200">
                  ATS PRO
                </span>
              </div>
            </Link>

            {/* Main Navigation Links */}
            <nav className="hidden md:flex items-center gap-1">
              <Link
                to="/jobs"
                className={`px-3.5 py-2 rounded-lg text-sm font-medium transition-colors ${
                  location.pathname === '/jobs'
                    ? 'text-brand-600 bg-brand-50/80 font-semibold'
                    : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
                }`}
              >
                Find Jobs
              </Link>
              <Link
                to="/pricing"
                className={`px-3.5 py-2 rounded-lg text-sm font-medium transition-colors ${
                  location.pathname === '/pricing'
                    ? 'text-brand-600 bg-brand-50/80 font-semibold'
                    : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
                }`}
              >
                SaaS Pricing
              </Link>

              {/* Candidate Quick Links */}
              {isAuthenticated && role === 'candidate' && (
                <>
                  <Link
                    to="/candidate/dashboard"
                    className={`px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                      location.pathname.startsWith('/candidate/dashboard')
                        ? 'text-brand-600 bg-brand-50 font-semibold'
                        : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
                    }`}
                  >
                    Dashboard
                  </Link>
                  <Link
                    to="/candidate/applications"
                    className={`px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                      location.pathname.startsWith('/candidate/applications')
                        ? 'text-brand-600 bg-brand-50 font-semibold'
                        : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
                    }`}
                  >
                    Applications
                  </Link>
                </>
              )}

              {/* Employer Quick Links */}
              {isAuthenticated && role === 'employer' && (
                <>
                  <Link
                    to="/employer/dashboard"
                    className={`px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                      location.pathname === '/employer/dashboard'
                        ? 'text-brand-600 bg-brand-50 font-semibold'
                        : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
                    }`}
                  >
                    ATS Workspace
                  </Link>
                  <Link
                    to="/employer/jobs"
                    className={`px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                      location.pathname === '/employer/jobs'
                        ? 'text-brand-600 bg-brand-50 font-semibold'
                        : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
                    }`}
                  >
                    Jobs & Post
                  </Link>
                  <Link
                    to="/employer/ats"
                    className={`px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                      location.pathname === '/employer/ats'
                        ? 'text-brand-600 bg-brand-50 font-semibold'
                        : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
                    }`}
                  >
                    Kanban Pipeline
                  </Link>
                  <Link
                    to="/employer/candidates"
                    className={`px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                      location.pathname === '/employer/candidates'
                        ? 'text-brand-600 bg-brand-50 font-semibold'
                        : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
                    }`}
                  >
                    Talent Search
                  </Link>
                </>
              )}

              {/* Admin Quick Links */}
              {isAuthenticated && (role === 'admin' || user?.is_staff) && (
                <>
                  <Link
                    to="/admin/dashboard"
                    className={`px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                      location.pathname === '/admin/dashboard'
                        ? 'text-brand-600 bg-brand-50 font-semibold'
                        : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
                    }`}
                  >
                    Admin Hub
                  </Link>
                  <Link
                    to="/admin/moderation"
                    className={`px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                      location.pathname === '/admin/moderation'
                        ? 'text-brand-600 bg-brand-50 font-semibold'
                        : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
                    }`}
                  >
                    Moderation
                  </Link>
                  <Link
                    to="/admin/verifications"
                    className={`px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                      location.pathname === '/admin/verifications'
                        ? 'text-brand-600 bg-brand-50 font-semibold'
                        : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
                    }`}
                  >
                    Verifications
                  </Link>
                </>
              )}
            </nav>
          </div>

          {/* Right Header Controls */}
          <div className="flex items-center gap-3">
            <button
              type="button"
              onClick={handleThemeToggle}
              className="p-2 rounded-xl text-slate-600 hover:text-slate-900 hover:bg-slate-100 transition-colors"
              aria-label={`Switch to ${isDark ? 'light' : 'night'} mode`}
              title={`Switch to ${isDark ? 'light' : 'night'} mode`}
            >
              {isDark ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
            </button>

            {/* Quick Demo Switcher Pill (Great for evaluation!) */}
            <div className="hidden lg:flex items-center gap-1 bg-slate-100/90 p-1 rounded-xl border border-slate-200 text-xs">
              <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider px-2">
                Demo
              </span>
              <button
                onClick={() => handleDemoSwitch('candidate')}
                className={`px-2.5 py-1 rounded-lg font-medium transition-all ${
                  role === 'candidate'
                    ? 'bg-white text-brand-700 shadow-sm font-semibold'
                    : 'text-slate-600 hover:text-slate-900 hover:bg-white/60'
                }`}
              >
                Candidate
              </button>
              <button
                onClick={() => handleDemoSwitch('employer')}
                className={`px-2.5 py-1 rounded-lg font-medium transition-all ${
                  role === 'employer'
                    ? 'bg-white text-brand-700 shadow-sm font-semibold'
                    : 'text-slate-600 hover:text-slate-900 hover:bg-white/60'
                }`}
              >
                Recruiter
              </button>
              <button
                onClick={() => handleDemoSwitch('admin')}
                className={`px-2.5 py-1 rounded-lg font-medium transition-all ${
                  role === 'admin'
                    ? 'bg-white text-brand-700 shadow-sm font-semibold'
                    : 'text-slate-600 hover:text-slate-900 hover:bg-white/60'
                }`}
              >
                Admin
              </button>
            </div>

            {/* Notifications Bell */}
            {isAuthenticated && (
              <div className="relative" ref={notifRef}>
                <button
                  onClick={() => setNotifDropdownOpen(!notifDropdownOpen)}
                  className="relative p-2 rounded-xl text-slate-600 hover:text-slate-900 hover:bg-slate-100 transition-colors"
                  aria-label="Notifications"
                >
                  <Bell className="w-5 h-5" />
                  {unreadCount > 0 && (
                    <span className="absolute top-1.5 right-1.5 w-4 h-4 rounded-full bg-rose-500 text-white text-[10px] font-bold flex items-center justify-center animate-pulse">
                      {unreadCount}
                    </span>
                  )}
                </button>

                {/* Notifications Dropdown */}
                {notifDropdownOpen && (
                  <div className="absolute right-0 mt-2 w-80 sm:w-96 rounded-2xl bg-white shadow-2xl border border-slate-200 overflow-hidden z-50 animate-fade-in">
                    <div className="p-3.5 bg-slate-50 border-b border-slate-200 flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <span className="font-semibold text-sm text-slate-800">Notifications</span>
                        {unreadCount > 0 && (
                          <span className="px-2 py-0.5 rounded-full text-xs font-semibold bg-brand-100 text-brand-700">
                            {unreadCount} new
                          </span>
                        )}
                      </div>
                      {unreadCount > 0 && (
                        <button
                          onClick={handleMarkAllRead}
                          className="text-xs text-brand-600 hover:text-brand-800 font-medium"
                        >
                          Mark all read
                        </button>
                      )}
                    </div>
                    <div className="max-h-80 overflow-y-auto divide-y divide-slate-100">
                      {notifications.length === 0 ? (
                        <div className="p-6 text-center text-xs text-slate-400">
                          No notifications yet.
                        </div>
                      ) : (
                        notifications.map((n) => (
                          <div
                            key={n.id}
                            className={`p-3.5 hover:bg-slate-50 transition-colors text-xs cursor-pointer ${
                              !n.is_read ? 'bg-brand-50/40 font-medium' : ''
                            }`}
                            onClick={() => {
                              if (n.action_url) navigate(n.action_url);
                              setNotifDropdownOpen(false);
                            }}
                          >
                            <p className="text-slate-900 font-semibold mb-0.5">{n.title}</p>
                            <p className="text-slate-600 leading-relaxed">{n.message}</p>
                            <span className="text-[10px] text-slate-400 mt-1 block">
                              {new Date(n.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                            </span>
                          </div>
                        ))
                      )}
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* User Profile or Login/Register */}
            {isAuthenticated ? (
              <div className="relative" ref={profileRef}>
                <button
                  onClick={() => setProfileDropdownOpen(!profileDropdownOpen)}
                  className="flex items-center gap-2.5 p-1.5 rounded-xl hover:bg-slate-100 transition-colors text-left"
                >
                  <img
                    src={user.display_avatar || `https://api.dicebear.com/7.x/avataaars/svg?seed=${user.email}`}
                    alt={user.first_name}
                    className="w-8 h-8 rounded-full ring-2 ring-brand-500/20 object-cover bg-slate-100"
                  />
                  <div className="hidden sm:block">
                    <p className="text-xs font-semibold text-slate-800 leading-tight">
                      {user.first_name || user.email.split('@')[0]}
                    </p>
                    <span className="text-[10px] font-medium text-slate-500 capitalize">
                      {user.role}
                    </span>
                  </div>
                  <ChevronDown className="w-3.5 h-3.5 text-slate-400 hidden sm:block" />
                </button>

                {/* Profile Dropdown */}
                {profileDropdownOpen && (
                  <div className="absolute right-0 mt-2 w-56 rounded-2xl bg-white shadow-2xl border border-slate-200 py-1.5 z-50 animate-fade-in text-sm text-slate-700">
                    <div className="px-4 py-2.5 border-b border-slate-100">
                      <p className="text-xs font-semibold text-slate-900 truncate">
                        {user.first_name} {user.last_name}
                      </p>
                      <p className="text-[11px] text-slate-500 truncate">{user.email}</p>
                      <span className="inline-block mt-1 px-2 py-0.5 rounded text-[10px] font-semibold bg-brand-50 text-brand-700 uppercase">
                        {user.role} Account
                      </span>
                    </div>

                    {role === 'candidate' && (
                      <>
                        <Link
                          to="/candidate/profile"
                          className="flex items-center gap-2 px-4 py-2 hover:bg-slate-50 text-xs text-slate-700"
                        >
                          <UserIcon className="w-4 h-4 text-slate-400" />
                          My Profile & CV
                        </Link>
                        <Link
                          to="/candidate/applications"
                          className="flex items-center gap-2 px-4 py-2 hover:bg-slate-50 text-xs text-slate-700"
                        >
                          <FileText className="w-4 h-4 text-slate-400" />
                          My Applications
                        </Link>
                        <Link
                          to="/candidate/saved"
                          className="flex items-center gap-2 px-4 py-2 hover:bg-slate-50 text-xs text-slate-700"
                        >
                          <Bookmark className="w-4 h-4 text-slate-400" />
                          Saved Jobs
                        </Link>
                      </>
                    )}

                    {role === 'employer' && (
                      <>
                        <Link
                          to="/employer/dashboard"
                          className="flex items-center gap-2 px-4 py-2 hover:bg-slate-50 text-xs text-slate-700"
                        >
                          <Building2 className="w-4 h-4 text-slate-400" />
                          Company ATS Hub
                        </Link>
                        <Link
                          to="/employer/team"
                          className="flex items-center gap-2 px-4 py-2 hover:bg-slate-50 text-xs text-slate-700"
                        >
                          <Users className="w-4 h-4 text-slate-400" />
                          Recruitment Team
                        </Link>
                        <Link
                          to="/employer/subscription"
                          className="flex items-center gap-2 px-4 py-2 hover:bg-slate-50 text-xs text-slate-700"
                        >
                          <CreditCard className="w-4 h-4 text-slate-400" />
                          SaaS Plan & Billing
                        </Link>
                      </>
                    )}

                    {(role === 'admin' || user?.is_staff) && (
                      <>
                        <Link
                          to="/admin/dashboard"
                          className="flex items-center gap-2 px-4 py-2 hover:bg-slate-50 text-xs text-slate-700"
                        >
                          <ShieldCheck className="w-4 h-4 text-slate-400" />
                          Admin Console
                        </Link>
                        <Link
                          to="/admin/audit-logs"
                          className="flex items-center gap-2 px-4 py-2 hover:bg-slate-50 text-xs text-slate-700"
                        >
                          <Layers className="w-4 h-4 text-slate-400" />
                          Security Audit Logs
                        </Link>
                      </>
                    )}

                    <div className="border-t border-slate-100 my-1"></div>
                    <button
                      onClick={handleLogout}
                      className="w-full flex items-center gap-2 px-4 py-2 text-rose-600 hover:bg-rose-50 text-xs text-left font-medium"
                    >
                      <LogOut className="w-4 h-4" />
                      Sign Out
                    </button>
                  </div>
                )}
              </div>
            ) : (
              <div className="flex items-center gap-2">
                <Link
                  to="/login"
                  className="px-3.5 py-1.5 rounded-xl text-xs font-medium text-slate-700 hover:text-slate-900 hover:bg-slate-100 transition-colors"
                >
                  Log In
                </Link>
                <Link
                  to="/register"
                  className="px-3.5 py-1.5 rounded-xl text-xs font-semibold bg-brand-600 text-white hover:bg-brand-700 shadow-sm shadow-brand-500/20 transition-colors"
                >
                  Get Started
                </Link>
              </div>
            )}

            {/* Mobile menu button */}
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="md:hidden p-2 rounded-xl text-slate-600 hover:bg-slate-100"
            >
              {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Drawer */}
      {mobileMenuOpen && (
        <div className="md:hidden border-t border-slate-200 bg-white px-4 pt-3 pb-6 space-y-3">
          {/* Quick Demo Switcher */}
          <div className="bg-slate-50 p-2.5 rounded-xl border border-slate-200">
            <span className="text-[11px] font-semibold text-slate-400 block mb-2">QUICK DEMO SWITCHER</span>
            <div className="grid grid-cols-3 gap-1.5 text-xs">
              <button
                onClick={() => handleDemoSwitch('candidate')}
                className="py-1.5 rounded-lg bg-white border border-slate-200 font-medium text-slate-700 text-center"
              >
                Candidate
              </button>
              <button
                onClick={() => handleDemoSwitch('employer')}
                className="py-1.5 rounded-lg bg-white border border-slate-200 font-medium text-slate-700 text-center"
              >
                Recruiter
              </button>
              <button
                onClick={() => handleDemoSwitch('admin')}
                className="py-1.5 rounded-lg bg-white border border-slate-200 font-medium text-slate-700 text-center"
              >
                Admin
              </button>
            </div>
          </div>

          <div className="space-y-1">
            <Link
              to="/jobs"
              className="block px-3 py-2 rounded-lg text-sm font-medium text-slate-700 hover:bg-slate-100"
            >
              Find Jobs
            </Link>
            <Link
              to="/pricing"
              className="block px-3 py-2 rounded-lg text-sm font-medium text-slate-700 hover:bg-slate-100"
            >
              SaaS Pricing
            </Link>
            {isAuthenticated && role === 'candidate' && (
              <>
                <Link
                  to="/candidate/dashboard"
                  className="block px-3 py-2 rounded-lg text-sm font-medium text-slate-700 hover:bg-slate-100"
                >
                  Candidate Dashboard
                </Link>
                <Link
                  to="/candidate/applications"
                  className="block px-3 py-2 rounded-lg text-sm font-medium text-slate-700 hover:bg-slate-100"
                >
                  My Applications
                </Link>
                <Link
                  to="/candidate/profile"
                  className="block px-3 py-2 rounded-lg text-sm font-medium text-slate-700 hover:bg-slate-100"
                >
                  Profile & CV
                </Link>
              </>
            )}
            {isAuthenticated && role === 'employer' && (
              <>
                <Link
                  to="/employer/dashboard"
                  className="block px-3 py-2 rounded-lg text-sm font-medium text-slate-700 hover:bg-slate-100"
                >
                  ATS Workspace
                </Link>
                <Link
                  to="/employer/jobs"
                  className="block px-3 py-2 rounded-lg text-sm font-medium text-slate-700 hover:bg-slate-100"
                >
                  Manage Jobs
                </Link>
                <Link
                  to="/employer/ats"
                  className="block px-3 py-2 rounded-lg text-sm font-medium text-slate-700 hover:bg-slate-100"
                >
                  Kanban Pipeline
                </Link>
              </>
            )}
            {isAuthenticated && (role === 'admin' || user?.is_staff) && (
              <>
                <Link
                  to="/admin/dashboard"
                  className="block px-3 py-2 rounded-lg text-sm font-medium text-slate-700 hover:bg-slate-100"
                >
                  Admin Console
                </Link>
                <Link
                  to="/admin/moderation"
                  className="block px-3 py-2 rounded-lg text-sm font-medium text-slate-700 hover:bg-slate-100"
                >
                  Moderation
                </Link>
              </>
            )}
          </div>
        </div>
      )}
    </header>
  );
};
