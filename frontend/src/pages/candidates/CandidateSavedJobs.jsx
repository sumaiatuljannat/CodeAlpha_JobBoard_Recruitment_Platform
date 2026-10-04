import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Bookmark, Briefcase, MapPin, Sparkles } from 'lucide-react';
import api from '../../api/client';

export const CandidateSavedJobs = () => {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchSavedJobs = async () => {
      try {
        const res = await api.get('/api/candidates/saved-jobs/');
        const list = res.data?.results || res.data || [];
        setJobs(list);
      } catch (err) {
        console.error('Failed to load saved jobs:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchSavedJobs();
  }, []);

  if (loading) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-10">
        <div className="animate-pulse space-y-4">
          <div className="h-10 w-48 rounded bg-slate-200" />
          <div className="grid gap-4 md:grid-cols-2">
            <div className="h-40 rounded-3xl bg-slate-200" />
            <div className="h-40 rounded-3xl bg-slate-200" />
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
      <div className="mb-8 flex items-center justify-between">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.2em] text-brand-600">Saved roles</p>
          <h1 className="mt-2 text-3xl font-black text-slate-900">Your shortlists</h1>
        </div>
        <Link to="/jobs" className="inline-flex items-center gap-2 rounded-xl bg-brand-600 px-4 py-2.5 text-sm font-semibold text-white hover:bg-brand-700">
          <Sparkles className="w-4 h-4" />
          Browse jobs
        </Link>
      </div>

      {jobs.length === 0 ? (
        <div className="rounded-3xl border border-dashed border-slate-300 bg-white p-10 text-center">
          <Bookmark className="mx-auto h-10 w-10 text-slate-300" />
          <h2 className="mt-4 text-xl font-bold text-slate-900">No saved jobs yet</h2>
          <p className="mt-2 text-sm text-slate-500">Save roles you like to track them here and compare fast.</p>
        </div>
      ) : (
        <div className="grid gap-5 md:grid-cols-2">
          {jobs.map((item) => {
            const job = item.job_details || item.job || {};
            return (
              <div key={item.id || job.id} className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
                <div className="flex items-start justify-between gap-4">
                  <div>
                    <p className="text-xs font-semibold uppercase tracking-[0.2em] text-brand-600">{job.company_name || 'Company'}</p>
                    <h2 className="mt-2 text-xl font-bold text-slate-900">{job.title}</h2>
                  </div>
                  <Bookmark className="h-5 w-5 text-brand-600" />
                </div>

                <div className="mt-4 flex flex-wrap gap-2 text-[11px] font-medium">
                  <span className="rounded-full bg-slate-100 px-2.5 py-1 text-slate-700">{job.employment_type || 'Full-time'}</span>
                  <span className="rounded-full bg-brand-50 px-2.5 py-1 text-brand-700">{job.workplace_type || 'Remote'}</span>
                  <span className="rounded-full bg-emerald-50 px-2.5 py-1 text-emerald-700">${Number(job.min_salary || 0).toLocaleString()}+</span>
                </div>

                <div className="mt-4 space-y-2 text-sm text-slate-600">
                  <div className="flex items-center gap-2"><MapPin className="h-4 w-4 text-slate-400" /> {job.location || 'Remote'}</div>
                  <div className="flex items-center gap-2"><Briefcase className="h-4 w-4 text-slate-400" /> {job.department || 'Engineering'}</div>
                </div>

                <p className="mt-4 line-clamp-3 text-sm text-slate-500">{job.description || 'No description available for this role.'}</p>

                <Link to={`/jobs/${job.slug || ''}`} className="mt-5 inline-flex items-center text-sm font-semibold text-brand-700 hover:text-brand-800">
                  View opportunity →
                </Link>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};
