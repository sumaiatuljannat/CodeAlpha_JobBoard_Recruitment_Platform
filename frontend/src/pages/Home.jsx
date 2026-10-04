import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import {
  Search,
  MapPin,
  Briefcase,
  Sparkles,
  Building2,
  TrendingUp,
  CheckCircle2,
  ArrowRight,
  ShieldCheck,
  Zap,
  Users,
  Clock,
  ChevronRight
} from 'lucide-react';
import api from '../api/client';
import { StatusBadge } from '../components/common/Badge';

export const Home = () => {
  const navigate = useNavigate();
  const [keyword, setKeyword] = useState('');
  const [location, setLocation] = useState('');
  const [featuredJobs, setFeaturedJobs] = useState([]);
  const [categories, setCategories] = useState([]);
  const [companies, setCompanies] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [jobsRes, catRes, compRes] = await Promise.all([
          api.get('/api/jobs/listings/featured/'),
          api.get('/api/jobs/categories/popular/'),
          api.get('/api/employers/companies/featured/'),
        ]);
        setFeaturedJobs(jobsRes.data || []);
        setCategories(catRes.data || []);
        setCompanies(compRes.data || []);
      } catch (err) {
        console.error('Failed to fetch home data:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const handleSearch = (e) => {
    e.preventDefault();
    const params = new URLSearchParams();
    if (keyword) params.append('search', keyword);
    if (location) params.append('location', location);
    navigate(`/jobs?${params.toString()}`);
  };

  return (
    <div className="space-y-16 pb-20">
      {/* Hero Section */}
      <section className="relative overflow-hidden bg-gradient-to-b from-brand-50/70 via-white to-white pt-12 pb-20 border-b border-slate-100">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center relative z-10">
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-brand-100/70 text-brand-800 text-xs font-semibold mb-6 border border-brand-200/60 shadow-sm animate-fade-in">
            <Sparkles className="w-3.5 h-3.5 text-brand-600" />
            <span>Next-Gen Recruitment Platform & Applicant Tracking System</span>
          </div>

          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-black text-slate-900 tracking-tight leading-tight max-w-4xl mx-auto">
            Hire Faster. Match Smarter.{' '}
            <span className="bg-gradient-to-r from-brand-600 to-indigo-600 bg-clip-text text-transparent">
              Elevate Careers.
            </span>
          </h1>

          <p className="mt-5 text-base sm:text-lg text-slate-600 max-w-2xl mx-auto leading-relaxed">
            HireFlow connects high-impact engineering, data science, and product teams with world-class professionals. Complete with AI-matching, visual ATS Kanban, and streamlined interviews.
          </p>

          {/* Search Bar Form */}
          <div className="mt-8 max-w-3xl mx-auto bg-white p-3 rounded-2xl shadow-xl border border-slate-200">
            <form onSubmit={handleSearch} className="flex flex-col sm:flex-row items-center gap-2">
              <div className="flex-1 flex items-center gap-2.5 px-3 py-2 w-full">
                <Search className="w-5 h-5 text-slate-400 shrink-0" />
                <input
                  type="text"
                  value={keyword}
                  onChange={(e) => setKeyword(e.target.value)}
                  placeholder="Job title, technical skill, or company..."
                  className="w-full bg-transparent text-sm text-slate-900 placeholder-slate-400 focus:outline-none"
                />
              </div>

              <div className="hidden sm:block w-px h-8 bg-slate-200"></div>

              <div className="flex-1 flex items-center gap-2.5 px-3 py-2 w-full">
                <MapPin className="w-5 h-5 text-slate-400 shrink-0" />
                <input
                  type="text"
                  value={location}
                  onChange={(e) => setLocation(e.target.value)}
                  placeholder="Location or 'Remote'..."
                  className="w-full bg-transparent text-sm text-slate-900 placeholder-slate-400 focus:outline-none"
                />
              </div>

              <button
                type="submit"
                className="w-full sm:w-auto px-6 py-3 rounded-xl bg-brand-600 hover:bg-brand-700 text-white font-semibold text-sm transition-colors shadow-md shadow-brand-500/20 flex items-center justify-center gap-2 shrink-0"
              >
                <span>Find Jobs</span>
                <ArrowRight className="w-4 h-4" />
              </button>
            </form>
          </div>

          {/* Popular searches pill */}
          <div className="mt-4 flex flex-wrap items-center justify-center gap-2 text-xs text-slate-500">
            <span className="font-semibold text-slate-400">Trending:</span>
            {['Python', 'React.js', 'Machine Learning', 'DevOps', 'Cybersecurity', 'Remote'].map((item) => (
              <button
                key={item}
                onClick={() => navigate(`/jobs?search=${encodeURIComponent(item)}`)}
                className="px-2.5 py-1 rounded-lg bg-slate-100 hover:bg-brand-50 hover:text-brand-700 text-slate-600 transition-colors"
              >
                {item}
              </button>
            ))}
          </div>

          {/* Stats Bar */}
          <div className="mt-14 grid grid-cols-2 md:grid-cols-4 gap-6 max-w-4xl mx-auto border-t border-slate-200/70 pt-8">
            <div className="text-left sm:text-center">
              <p className="text-3xl font-extrabold text-slate-900">110+</p>
              <p className="text-xs font-medium text-slate-500 mt-0.5">Active Job Listings</p>
            </div>
            <div className="text-left sm:text-center">
              <p className="text-3xl font-extrabold text-brand-600">22</p>
              <p className="text-xs font-medium text-slate-500 mt-0.5">Verified Enterprises</p>
            </div>
            <div className="text-left sm:text-center">
              <p className="text-3xl font-extrabold text-slate-900">96%</p>
              <p className="text-xs font-medium text-slate-500 mt-0.5">Profile Match Accuracy</p>
            </div>
            <div className="text-left sm:text-center">
              <p className="text-3xl font-extrabold text-emerald-600">18 Days</p>
              <p className="text-xs font-medium text-slate-500 mt-0.5">Avg Time-to-Hire</p>
            </div>
          </div>
        </div>
      </section>

      {/* Featured Categories */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h2 className="text-2xl font-bold text-slate-900">Explore by Department</h2>
            <p className="text-xs text-slate-500 mt-0.5">Browse opportunities curated across top technology disciplines</p>
          </div>
          <Link to="/jobs" className="text-xs font-semibold text-brand-600 hover:text-brand-800 flex items-center gap-1">
            <span>View All</span>
            <ChevronRight className="w-3.5 h-3.5" />
          </Link>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
          {categories.map((cat) => (
            <div
              key={cat.id}
              onClick={() => navigate(`/jobs?category=${cat.id}`)}
              className="p-5 rounded-2xl bg-white border border-slate-200 hover:border-brand-500 hover:shadow-lg transition-all cursor-pointer group"
            >
              <div className="w-10 h-10 rounded-xl bg-brand-50 text-brand-600 flex items-center justify-center mb-3 group-hover:scale-110 transition-transform">
                <Briefcase className="w-5 h-5" />
              </div>
              <h3 className="font-semibold text-sm text-slate-900 group-hover:text-brand-600 transition-colors">
                {cat.name}
              </h3>
              <p className="text-xs text-slate-400 mt-1 line-clamp-2">{cat.description || 'Top opportunities available.'}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Featured Jobs Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between mb-8">
          <div>
            <div className="flex items-center gap-2">
              <h2 className="text-2xl font-bold text-slate-900">Featured Openings</h2>
              <span className="px-2 py-0.5 rounded-full text-[11px] font-semibold bg-emerald-100 text-emerald-800 border border-emerald-200">
                Verified
              </span>
            </div>
            <p className="text-xs text-slate-500 mt-0.5">High-priority positions hand-picked for quality and competitive compensation</p>
          </div>
          <Link to="/jobs" className="text-xs font-semibold text-brand-600 hover:text-brand-800 flex items-center gap-1">
            <span>Explore 100+ Jobs</span>
            <ChevronRight className="w-3.5 h-3.5" />
          </Link>
        </div>

        {loading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[1, 2, 3, 4, 5, 6].map((i) => (
              <div key={i} className="h-48 rounded-2xl bg-slate-100 animate-pulse"></div>
            ))}
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {featuredJobs.map((job) => (
              <div
                key={job.id}
                onClick={() => navigate(`/jobs/${job.slug}`)}
                className="p-6 rounded-2xl bg-white border border-slate-200 hover:border-brand-500 hover:shadow-xl transition-all cursor-pointer flex flex-col justify-between group"
              >
                <div>
                  <div className="flex items-start justify-between gap-4 mb-3">
                    <div className="flex items-center gap-3">
                      <img
                        src={job.company_logo || 'https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=100&auto=format&fit=crop&q=80'}
                        alt={job.company_name}
                        className="w-11 h-11 rounded-xl object-cover border border-slate-100 bg-slate-50"
                      />
                      <div>
                        <h4 className="font-semibold text-xs text-slate-500 flex items-center gap-1">
                          <span>{job.company_name}</span>
                          {job.is_company_verified && (
                            <ShieldCheck className="w-3.5 h-3.5 text-brand-500" />
                          )}
                        </h4>
                        <h3 className="font-bold text-sm text-slate-900 group-hover:text-brand-600 transition-colors line-clamp-1">
                          {job.title}
                        </h3>
                      </div>
                    </div>
                  </div>

                  <div className="flex flex-wrap items-center gap-1.5 mb-4">
                    <span className="px-2 py-0.5 rounded-md text-[11px] font-medium bg-slate-100 text-slate-700">
                      {job.workplace_type === 'remote' ? '🌐 Remote' : job.location}
                    </span>
                    <span className="px-2 py-0.5 rounded-md text-[11px] font-medium bg-brand-50 text-brand-700">
                      {job.employment_type?.replace('_', ' ').toUpperCase()}
                    </span>
                    <span className="px-2 py-0.5 rounded-md text-[11px] font-medium bg-emerald-50 text-emerald-700 font-semibold">
                      ${Number(job.min_salary || 0).toLocaleString()} - ${Number(job.max_salary || 0).toLocaleString()}
                    </span>
                  </div>

                  <p className="text-xs text-slate-500 line-clamp-2 mb-4 leading-relaxed">
                    {job.description}
                  </p>
                </div>

                <div className="pt-4 border-t border-slate-100 flex items-center justify-between text-xs text-slate-400">
                  <span>{job.applications_count || 0} applicants</span>
                  <span className="font-semibold text-brand-600 group-hover:translate-x-0.5 transition-transform flex items-center gap-0.5">
                    View Details →
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}
      </section>

      {/* Featured Companies */}
      <section className="bg-slate-50 py-16 border-y border-slate-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-2xl mx-auto mb-12">
            <h2 className="text-2xl font-bold text-slate-900">Trusted by Industry Innovators</h2>
            <p className="text-xs text-slate-500 mt-1">Leading software, fintech, and AI enterprises actively building teams on HireFlow</p>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-6">
            {companies.map((c) => (
              <div
                key={c.id}
                onClick={() => navigate(`/jobs?company=${c.id}`)}
                className="p-5 rounded-2xl bg-white border border-slate-200 hover:border-brand-500 hover:shadow-md transition-all cursor-pointer flex flex-col items-center text-center group"
              >
                <img
                  src={c.display_logo || c.logo_url}
                  alt={c.name}
                  className="w-14 h-14 rounded-2xl object-cover mb-3 border border-slate-100 shadow-sm"
                />
                <h4 className="font-bold text-sm text-slate-900 group-hover:text-brand-600 transition-colors flex items-center gap-1">
                  <span>{c.name}</span>
                  {c.is_verified && <ShieldCheck className="w-4 h-4 text-brand-500 shrink-0" />}
                </h4>
                <p className="text-xs text-slate-500 mt-0.5">{c.industry}</p>
                <span className="mt-3 text-[11px] font-semibold text-brand-600 bg-brand-50 px-2.5 py-1 rounded-full">
                  {c.active_jobs_count || 0} Open Roles
                </span>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Platform Showcase */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="rounded-3xl bg-gradient-to-r from-slate-900 via-brand-950 to-slate-900 text-white p-8 sm:p-14 shadow-2xl relative overflow-hidden">
          <div className="relative z-10 max-w-2xl">
            <span className="px-3 py-1 rounded-full bg-brand-500/20 text-brand-300 text-xs font-semibold uppercase tracking-wider border border-brand-500/30">
              For Growing Teams & Enterprises
            </span>
            <h2 className="text-3xl sm:text-4xl font-black tracking-tight mt-4">
              Supercharge your talent acquisition pipeline today
            </h2>
            <p className="text-slate-300 text-sm mt-3 leading-relaxed">
              From job broadcasting to resume parsing, automated Kanban stage progression, and interview invitations — manage your end-to-end recruitment seamlessly.
            </p>
            <div className="mt-8 flex flex-wrap gap-4">
              <Link
                to="/register"
                className="px-6 py-3 rounded-xl bg-brand-500 hover:bg-brand-600 text-white font-semibold text-sm transition-colors shadow-lg shadow-brand-500/30"
              >
                Start Hiring on HireFlow
              </Link>
              <Link
                to="/pricing"
                className="px-6 py-3 rounded-xl bg-white/10 hover:bg-white/20 text-white font-semibold text-sm transition-colors border border-white/20"
              >
                Explore SaaS Plans
              </Link>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};
