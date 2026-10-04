import React, { useState, useEffect } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import {
  Search,
  MapPin,
  Briefcase,
  Filter,
  DollarSign,
  Bookmark,
  Building2,
  ShieldCheck,
  ChevronLeft,
  ChevronRight,
  Clock,
  Sparkles,
  RotateCcw
} from 'lucide-react';
import api from '../../api/client';
import { useAuth } from '../../context/AuthContext';
import { useToast } from '../../context/ToastContext';

export const JobSearch = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const navigate = useNavigate();
  const { user, isAuthenticated } = useAuth();
  const { success, error, info } = useToast();

  const [jobs, setJobs] = useState([]);
  const [categories, setCategories] = useState([]);
  const [totalCount, setTotalCount] = useState(0);
  const [loading, setLoading] = useState(true);
  const [savedJobIds, setSavedJobIds] = useState(new Set());

  // Filter States
  const [search, setSearch] = useState(searchParams.get('search') || '');
  const [location, setLocation] = useState(searchParams.get('location') || '');
  const [selectedCategory, setSelectedCategory] = useState(searchParams.get('category') || '');
  const [employmentType, setEmploymentType] = useState(searchParams.get('employment_type') || '');
  const [workplaceType, setWorkplaceType] = useState(searchParams.get('workplace_type') || '');
  const [experienceLevel, setExperienceLevel] = useState(searchParams.get('experience_level') || '');
  const [ordering, setOrdering] = useState(searchParams.get('ordering') || '-created_at');
  const [page, setPage] = useState(Number(searchParams.get('page')) || 1);

  // Fetch categories on mount
  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const res = await api.get('/api/jobs/categories/');
        setCategories(res.data?.results || res.data || []);
      } catch (err) {
        console.error(err);
      }
    };
    fetchCategories();
  }, []);

  // Fetch saved jobs if candidate
  useEffect(() => {
    if (isAuthenticated && user?.role === 'candidate') {
      api.get('/api/candidates/saved-jobs/').then((res) => {
        const list = res.data?.results || res.data || [];
        const ids = new Set(list.map((item) => item.job?.id || item.job));
        setSavedJobIds(ids);
      }).catch(() => {});
    }
  }, [isAuthenticated, user]);

  // Main fetch jobs function
  const fetchJobs = async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      if (search) params.append('search', search);
      if (location) params.append('location', location);
      if (selectedCategory) params.append('category', selectedCategory);
      if (employmentType) params.append('employment_type', employmentType);
      if (workplaceType) params.append('workplace_type', workplaceType);
      if (experienceLevel) params.append('experience_level', experienceLevel);
      if (ordering) params.append('ordering', ordering);
      params.append('page', page);

      setSearchParams(params, { replace: true });

      const res = await api.get(`/api/jobs/listings/?${params.toString()}`);
      if (res.data?.results) {
        setJobs(res.data.results);
        setTotalCount(res.data.count || res.data.results.length);
      } else {
        setJobs(res.data || []);
        setTotalCount(res.data?.length || 0);
      }
    } catch (err) {
      console.error(err);
      error('Failed to load job listings.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchJobs();
  }, [selectedCategory, employmentType, workplaceType, experienceLevel, ordering, page]);

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    setPage(1);
    fetchJobs();
  };

  const handleResetFilters = () => {
    setSearch('');
    setLocation('');
    setSelectedCategory('');
    setEmploymentType('');
    setWorkplaceType('');
    setExperienceLevel('');
    setOrdering('-created_at');
    setPage(1);
  };

  const handleToggleSave = async (e, jobId) => {
    e.stopPropagation();
    if (!isAuthenticated) {
      info('Please sign in as a candidate to bookmark jobs.');
      navigate('/login');
      return;
    }
    try {
      const res = await api.post('/api/candidates/saved-jobs/toggle/', { job_id: jobId });
      if (res.data?.is_saved) {
        setSavedJobIds((prev) => new Set([...prev, jobId]));
        success('Job saved to your bookmarks.');
      } else {
        setSavedJobIds((prev) => {
          const next = new Set(prev);
          next.delete(jobId);
          return next;
        });
        info('Job removed from bookmarks.');
      }
    } catch (err) {
      error('Failed to update saved job.');
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
      {/* Search Header Banner */}
      <div className="bg-white p-6 rounded-3xl border border-slate-200 shadow-sm">
        <form onSubmit={handleSearchSubmit} className="flex flex-col md:flex-row items-center gap-3">
          <div className="flex-1 flex items-center gap-2.5 px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-2xl w-full">
            <Search className="w-5 h-5 text-slate-400 shrink-0" />
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search by title, technical skill, or keyword..."
              className="w-full bg-transparent text-sm text-slate-900 placeholder-slate-400 focus:outline-none"
            />
          </div>

          <div className="flex-1 flex items-center gap-2.5 px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-2xl w-full">
            <MapPin className="w-5 h-5 text-slate-400 shrink-0" />
            <input
              type="text"
              value={location}
              onChange={(e) => setLocation(e.target.value)}
              placeholder="Location, city, or 'Remote'..."
              className="w-full bg-transparent text-sm text-slate-900 placeholder-slate-400 focus:outline-none"
            />
          </div>

          <button
            type="submit"
            className="w-full md:w-auto px-7 py-3 rounded-2xl bg-brand-600 hover:bg-brand-700 text-white font-semibold text-sm transition-colors shadow-md shadow-brand-500/20 shrink-0"
          >
            Search Jobs
          </button>
        </form>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-8 items-start">
        {/* Left Filter Sidebar */}
        <div className="bg-white p-6 rounded-3xl border border-slate-200 shadow-sm space-y-6 lg:sticky lg:top-24">
          <div className="flex items-center justify-between pb-3 border-b border-slate-100">
            <div className="flex items-center gap-2 font-bold text-sm text-slate-900">
              <Filter className="w-4 h-4 text-brand-600" />
              <span>Filters</span>
            </div>
            <button
              onClick={handleResetFilters}
              className="text-xs text-slate-400 hover:text-slate-700 flex items-center gap-1"
            >
              <RotateCcw className="w-3 h-3" />
              <span>Reset</span>
            </button>
          </div>

          {/* Department / Category */}
          <div>
            <label className="block text-xs font-bold text-slate-800 uppercase tracking-wider mb-2">
              Department
            </label>
            <select
              value={selectedCategory}
              onChange={(e) => {
                setSelectedCategory(e.target.value);
                setPage(1);
              }}
              className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-700 focus:outline-none focus:ring-2 focus:ring-brand-500/20"
            >
              <option value="">All Categories</option>
              {categories.map((c) => (
                <option key={c.id} value={c.id}>
                  {c.name}
                </option>
              ))}
            </select>
          </div>

          {/* Workplace Type */}
          <div>
            <label className="block text-xs font-bold text-slate-800 uppercase tracking-wider mb-2">
              Workplace Type
            </label>
            <div className="space-y-1.5 text-xs text-slate-600">
              {[
                { value: '', label: 'All Workplace Types' },
                { value: 'remote', label: '🌐 Remote' },
                { value: 'hybrid', label: '🏢 Hybrid' },
                { value: 'on_site', label: '📍 On-site' },
              ].map((item) => (
                <label key={item.value} className="flex items-center gap-2 cursor-pointer">
                  <input
                    type="radio"
                    name="workplace_type"
                    value={item.value}
                    checked={workplaceType === item.value}
                    onChange={(e) => {
                      setWorkplaceType(e.target.value);
                      setPage(1);
                    }}
                    className="text-brand-600 focus:ring-brand-500"
                  />
                  <span>{item.label}</span>
                </label>
              ))}
            </div>
          </div>

          {/* Employment Type */}
          <div>
            <label className="block text-xs font-bold text-slate-800 uppercase tracking-wider mb-2">
              Employment Type
            </label>
            <div className="space-y-1.5 text-xs text-slate-600">
              {[
                { value: '', label: 'All Types' },
                { value: 'full_time', label: 'Full-time' },
                { value: 'contract', label: 'Contract' },
                { value: 'part_time', label: 'Part-time' },
                { value: 'internship', label: 'Internship' },
              ].map((item) => (
                <label key={item.value} className="flex items-center gap-2 cursor-pointer">
                  <input
                    type="radio"
                    name="employment_type"
                    value={item.value}
                    checked={employmentType === item.value}
                    onChange={(e) => {
                      setEmploymentType(e.target.value);
                      setPage(1);
                    }}
                    className="text-brand-600 focus:ring-brand-500"
                  />
                  <span>{item.label}</span>
                </label>
              ))}
            </div>
          </div>

          {/* Experience Level */}
          <div>
            <label className="block text-xs font-bold text-slate-800 uppercase tracking-wider mb-2">
              Experience Level
            </label>
            <div className="space-y-1.5 text-xs text-slate-600">
              {[
                { value: '', label: 'Any Experience' },
                { value: 'entry', label: 'Entry Level (0-1 yrs)' },
                { value: 'junior', label: 'Junior (1-3 yrs)' },
                { value: 'mid', label: 'Mid Level (3-5 yrs)' },
                { value: 'senior', label: 'Senior (5-8 yrs)' },
                { value: 'lead', label: 'Lead / Principal (8+ yrs)' },
              ].map((item) => (
                <label key={item.value} className="flex items-center gap-2 cursor-pointer">
                  <input
                    type="radio"
                    name="experience_level"
                    value={item.value}
                    checked={experienceLevel === item.value}
                    onChange={(e) => {
                      setExperienceLevel(e.target.value);
                      setPage(1);
                    }}
                    className="text-brand-600 focus:ring-brand-500"
                  />
                  <span>{item.label}</span>
                </label>
              ))}
            </div>
          </div>
        </div>

        {/* Right Job List */}
        <div className="lg:col-span-3 space-y-4">
          {/* Header Bar */}
          <div className="bg-white px-5 py-3.5 rounded-2xl border border-slate-200 shadow-sm flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs">
            <span className="font-semibold text-slate-700">
              Showing <span className="text-brand-600 font-bold">{totalCount}</span> Available Positions
            </span>

            <div className="flex items-center gap-2">
              <span className="text-slate-400">Sort by:</span>
              <select
                value={ordering}
                onChange={(e) => {
                  setOrdering(e.target.value);
                  setPage(1);
                }}
                className="bg-slate-50 border border-slate-200 rounded-lg px-2.5 py-1 text-slate-700 font-medium focus:outline-none"
              >
                <option value="-created_at">Newest First</option>
                <option value="-min_salary">Highest Salary</option>
                <option value="-views_count">Most Viewed</option>
              </select>
            </div>
          </div>

          {/* Cards List */}
          {loading ? (
            <div className="space-y-4">
              {[1, 2, 3, 4, 5].map((i) => (
                <div key={i} className="h-36 rounded-2xl bg-slate-100 animate-pulse"></div>
              ))}
            </div>
          ) : jobs.length === 0 ? (
            <div className="bg-white p-12 text-center rounded-3xl border border-slate-200">
              <Briefcase className="w-12 h-12 text-slate-300 mx-auto mb-3" />
              <h3 className="font-bold text-base text-slate-800">No positions matched your query</h3>
              <p className="text-xs text-slate-500 mt-1 max-w-sm mx-auto">
                Try expanding your search criteria or resetting filters to view all available listings.
              </p>
              <button
                onClick={handleResetFilters}
                className="mt-4 px-4 py-2 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-semibold"
              >
                Reset All Filters
              </button>
            </div>
          ) : (
            jobs.map((job) => {
              const isSaved = savedJobIds.has(job.id);
              return (
                <div
                  key={job.id}
                  onClick={() => navigate(`/jobs/${job.slug}`)}
                  className="p-5 sm:p-6 rounded-2xl bg-white border border-slate-200 hover:border-brand-500 hover:shadow-lg transition-all cursor-pointer group relative"
                >
                  <div className="flex items-start justify-between gap-4">
                    <div className="flex items-start gap-4">
                      <img
                        src={job.company_logo || 'https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=100&auto=format&fit=crop&q=80'}
                        alt={job.company_name}
                        className="w-12 h-12 rounded-xl object-cover border border-slate-100 bg-slate-50 shrink-0"
                      />
                      <div>
                        <div className="flex items-center gap-1.5 text-xs text-slate-500 mb-0.5">
                          <span className="font-semibold">{job.company_name}</span>
                          {job.is_company_verified && (
                            <ShieldCheck className="w-3.5 h-3.5 text-brand-600" />
                          )}
                          <span>•</span>
                          <span>{job.workplace_type === 'remote' ? '🌐 Remote' : job.location}</span>
                        </div>
                        <h3 className="text-base font-bold text-slate-900 group-hover:text-brand-600 transition-colors">
                          {job.title}
                        </h3>
                      </div>
                    </div>

                    {/* Bookmark action */}
                    <button
                      type="button"
                      onClick={(e) => handleToggleSave(e, job.id)}
                      className={`p-2 rounded-xl border transition-colors ${
                        isSaved
                          ? 'bg-brand-50 border-brand-200 text-brand-600'
                          : 'bg-slate-50 border-slate-200 text-slate-400 hover:text-slate-700'
                      }`}
                      title={isSaved ? 'Saved to bookmarks' : 'Bookmark job'}
                    >
                      <Bookmark className={`w-4 h-4 ${isSaved ? 'fill-current' : ''}`} />
                    </button>
                  </div>

                  <p className="mt-3 text-xs text-slate-500 line-clamp-2 leading-relaxed">
                    {job.description}
                  </p>

                  {/* Skills tags */}
                  {job.job_skills && job.job_skills.length > 0 && (
                    <div className="mt-3 flex flex-wrap items-center gap-1.5">
                      {job.job_skills.slice(0, 5).map((js, idx) => (
                        <span
                          key={idx}
                          className="px-2 py-0.5 rounded-md text-[11px] font-medium bg-slate-100 text-slate-600"
                        >
                          {js.skill?.name || js}
                        </span>
                      ))}
                    </div>
                  )}

                  {/* Bottom details */}
                  <div className="mt-4 pt-3.5 border-t border-slate-100 flex flex-wrap items-center justify-between gap-3 text-xs">
                    <div className="flex items-center gap-2">
                      <span className="px-2.5 py-1 rounded-lg text-xs font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200">
                        ${Number(job.min_salary || 0).toLocaleString()} - ${Number(job.max_salary || 0).toLocaleString()} / yr
                      </span>
                      <span className="px-2 py-0.5 rounded text-[11px] font-medium bg-brand-50 text-brand-700 capitalize">
                        {job.employment_type?.replace('_', ' ')}
                      </span>
                    </div>

                    <div className="flex items-center gap-3 text-slate-400 text-[11px]">
                      <span>{job.applications_count || 0} applicants</span>
                      <span>•</span>
                      <span>{new Date(job.created_at).toLocaleDateString()}</span>
                    </div>
                  </div>
                </div>
              );
            })
          )}

          {/* Pagination */}
          {totalCount > 12 && (
            <div className="flex items-center justify-center gap-2 pt-4">
              <button
                onClick={() => setPage((p) => Math.max(1, p - 1))}
                disabled={page <= 1}
                className="px-3.5 py-2 rounded-xl bg-white border border-slate-200 text-xs font-medium disabled:opacity-50 flex items-center gap-1"
              >
                <ChevronLeft className="w-3.5 h-3.5" />
                Previous
              </button>
              <span className="text-xs font-semibold text-slate-600 px-3">
                Page {page} of {Math.ceil(totalCount / 12)}
              </span>
              <button
                onClick={() => setPage((p) => p + 1)}
                disabled={page >= Math.ceil(totalCount / 12)}
                className="px-3.5 py-2 rounded-xl bg-white border border-slate-200 text-xs font-medium disabled:opacity-50 flex items-center gap-1"
              >
                Next
                <ChevronRight className="w-3.5 h-3.5" />
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
