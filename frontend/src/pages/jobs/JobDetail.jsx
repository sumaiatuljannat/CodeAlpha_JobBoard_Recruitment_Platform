import React, { useEffect, useMemo, useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import {
  ArrowLeft,
  Briefcase,
  Building2,
  CalendarDays,
  Clock3,
  DollarSign,
  MapPin,
  ShieldCheck,
  Sparkles,
} from 'lucide-react';
import api from '../../api/client';
import { useAuth } from '../../context/AuthContext';
import { useToast } from '../../context/ToastContext';

export const JobDetail = () => {
  const { slug } = useParams();
  const navigate = useNavigate();
  const { isAuthenticated, isCandidate } = useAuth();
  const { success, error, info } = useToast();

  const [job, setJob] = useState(null);
  const [loading, setLoading] = useState(true);
  const [coverLetter, setCoverLetter] = useState('');
  const [expectedSalary, setExpectedSalary] = useState('');
  const [availabilityNotice, setAvailabilityNotice] = useState('Immediate');
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    const fetchJob = async () => {
      try {
        setLoading(true);
        const res = await api.get(`/api/jobs/listings/${slug}/`);
        setJob(res.data);
      } catch (err) {
        console.error(err);
        error('This job is no longer available.');
      } finally {
        setLoading(false);
      }
    };

    if (slug) fetchJob();
  }, [slug, error]);

  const salaryText = useMemo(() => {
    if (!job) return 'Competitive package';
    if (job.min_salary || job.max_salary) {
      const min = Number(job.min_salary || 0);
      const max = Number(job.max_salary || 0);
      return `$${min.toLocaleString()} - $${max.toLocaleString()} / year`;
    }
    return 'Competitive package';
  }, [job]);

  const handleApply = async () => {
    if (!isAuthenticated) {
      info('Please sign in to apply for this role.');
      navigate('/login');
      return;
    }

    if (!isCandidate) {
      info('Only candidates can submit applications.');
      return;
    }

    if (!job) return;

    try {
      setSubmitting(true);
      await api.post('/api/applications/', {
        job: job.id,
        cover_letter: coverLetter,
        expected_salary: expectedSalary || null,
        availability_notice: availabilityNotice,
      });

      success('Application submitted successfully.');
      navigate('/candidate/applications');
    } catch (err) {
      const message =
        err.response?.data?.detail ||
        err.response?.data?.non_field_errors?.[0] ||
        'Unable to submit application right now.';
      error(message);
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        <div className="animate-pulse space-y-6">
          <div className="h-8 w-40 rounded bg-slate-200" />
          <div className="h-48 rounded-3xl bg-slate-200" />
          <div className="h-24 rounded-3xl bg-slate-200" />
        </div>
      </div>
    );
  }

  if (!job) {
    return (
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-16 text-center">
        <Briefcase className="w-14 h-14 mx-auto text-slate-300" />
        <h1 className="mt-4 text-2xl font-bold text-slate-900">Job not found</h1>
        <p className="mt-2 text-sm text-slate-500">This role may have expired or been removed.</p>
        <Link to="/jobs" className="mt-6 inline-flex items-center rounded-xl bg-brand-600 px-4 py-2 text-sm font-semibold text-white">
          Browse jobs
        </Link>
      </div>
    );
  }

  const companyLogo = job.company?.display_logo || 'https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=100&auto=format&fit=crop&q=80';
  const companyName = job.company?.name || 'Company';

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-6">
        <Link to="/jobs" className="inline-flex items-center gap-2 text-sm font-medium text-slate-600 hover:text-slate-900">
          <ArrowLeft className="w-4 h-4" />
          Back to jobs
        </Link>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-[1.45fr_0.75fr] gap-8">
        <div className="space-y-6">
          <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
            <div className="flex items-start gap-4">
              <img src={companyLogo} alt={companyName} className="h-16 w-16 rounded-2xl object-cover border border-slate-200" />
              <div className="flex-1">
                <div className="flex flex-wrap items-center gap-2 text-xs text-slate-500">
                  <span className="font-semibold text-slate-700">{companyName}</span>
                  {job.company?.is_verified && <ShieldCheck className="h-4 w-4 text-brand-600" />}
                  <span>•</span>
                  <span>{job.company?.industry || 'Technology'}</span>
                </div>
                <h1 className="mt-2 text-3xl font-black text-slate-900">{job.title}</h1>
                <div className="mt-3 flex flex-wrap items-center gap-4 text-sm text-slate-600">
                  <span className="inline-flex items-center gap-2"><MapPin className="h-4 w-4 text-slate-400" /> {job.location}</span>
                  <span className="inline-flex items-center gap-2"><Clock3 className="h-4 w-4 text-slate-400" /> {job.employment_type?.replace('_', ' ')}</span>
                  <span className="inline-flex items-center gap-2"><Building2 className="h-4 w-4 text-slate-400" /> {job.workplace_type?.replace('_', ' ')}</span>
                </div>
              </div>
            </div>
          </div>

          <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
            <div className="flex flex-wrap items-center gap-3 mb-5">
              <span className="inline-flex items-center gap-2 rounded-full bg-emerald-50 px-3 py-1.5 text-xs font-semibold text-emerald-700 border border-emerald-200">
                <Sparkles className="h-3.5 w-3.5" />
                {job.status === 'published' ? 'Hiring now' : job.status}
              </span>
              <span className="inline-flex items-center gap-2 rounded-full bg-brand-50 px-3 py-1.5 text-xs font-semibold text-brand-700 border border-brand-200">
                <DollarSign className="h-3.5 w-3.5" />
                {salaryText}
              </span>
            </div>

            <div className="space-y-6">
              <section>
                <h2 className="text-lg font-bold text-slate-900">Role overview</h2>
                <p className="mt-3 text-sm leading-7 text-slate-600">{job.description}</p>
              </section>

              <section>
                <h2 className="text-lg font-bold text-slate-900">Responsibilities</h2>
                <ul className="mt-3 space-y-2 text-sm text-slate-600">
                  {(job.responsibilities || []).map((item, index) => (
                    <li key={index} className="flex gap-2"><span className="mt-1.5 h-1.5 w-1.5 rounded-full bg-brand-600" />{item}</li>
                  ))}
                </ul>
              </section>

              <section>
                <h2 className="text-lg font-bold text-slate-900">Requirements</h2>
                <ul className="mt-3 space-y-2 text-sm text-slate-600">
                  {(job.requirements || []).map((item, index) => (
                    <li key={index} className="flex gap-2"><span className="mt-1.5 h-1.5 w-1.5 rounded-full bg-slate-400" />{item}</li>
                  ))}
                </ul>
              </section>

              <section>
                <h2 className="text-lg font-bold text-slate-900">Perks & benefits</h2>
                <div className="mt-3 flex flex-wrap gap-2">
                  {(job.benefits || []).map((benefit, index) => (
                    <span key={index} className="rounded-full border border-slate-200 bg-slate-50 px-3 py-1.5 text-xs font-medium text-slate-700">{benefit}</span>
                  ))}
                </div>
              </section>
            </div>
          </div>
        </div>

        <aside className="space-y-6">
          <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
            <div className="flex items-center justify-between gap-3">
              <div>
                <p className="text-xs font-semibold uppercase tracking-[0.2em] text-slate-500">Quick facts</p>
                <h3 className="mt-2 text-xl font-bold text-slate-900">Role details</h3>
              </div>
            </div>
            <div className="mt-5 space-y-4 text-sm text-slate-600">
              <div className="flex justify-between gap-3 border-b border-slate-100 pb-3">
                <span>Experience</span>
                <span className="font-semibold text-slate-800">{job.experience_level}</span>
              </div>
              <div className="flex justify-between gap-3 border-b border-slate-100 pb-3">
                <span>Education</span>
                <span className="font-semibold text-slate-800">{job.education_level}</span>
              </div>
              <div className="flex justify-between gap-3 border-b border-slate-100 pb-3">
                <span>Vacancies</span>
                <span className="font-semibold text-slate-800">{job.vacancies}</span>
              </div>
              <div className="flex justify-between gap-3 pb-1">
                <span>Deadline</span>
                <span className="font-semibold text-slate-800">{job.deadline ? new Date(job.deadline).toLocaleDateString() : 'Open until filled'}</span>
              </div>
            </div>

            <div className="mt-6 flex flex-wrap gap-2">
              {(job.skills || []).map((skill, index) => (
                <span key={index} className="rounded-full bg-slate-100 px-2.5 py-1 text-[11px] font-medium text-slate-700">
                  {skill.skill_name || skill.name || skill}
                </span>
              ))}
            </div>
          </div>

          <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
            <p className="text-xs font-semibold uppercase tracking-[0.2em] text-slate-500">Apply now</p>
            <h3 className="mt-2 text-xl font-bold text-slate-900">Submit your application</h3>

            <div className="mt-4 space-y-3">
              <div>
                <label className="mb-2 block text-xs font-semibold uppercase tracking-wide text-slate-600">Expected salary</label>
                <input
                  value={expectedSalary}
                  onChange={(e) => setExpectedSalary(e.target.value)}
                  placeholder="e.g. 120000"
                  className="w-full rounded-xl border border-slate-200 bg-slate-50 px-3 py-2.5 text-sm text-slate-800 outline-none focus:border-brand-400"
                />
              </div>
              <div>
                <label className="mb-2 block text-xs font-semibold uppercase tracking-wide text-slate-600">Availability</label>
                <select
                  value={availabilityNotice}
                  onChange={(e) => setAvailabilityNotice(e.target.value)}
                  className="w-full rounded-xl border border-slate-200 bg-slate-50 px-3 py-2.5 text-sm text-slate-800 outline-none focus:border-brand-400"
                >
                  <option value="Immediate">Immediate</option>
                  <option value="2 weeks">2 weeks</option>
                  <option value="1 month">1 month</option>
                  <option value="Negotiable">Negotiable</option>
                </select>
              </div>
              <div>
                <label className="mb-2 block text-xs font-semibold uppercase tracking-wide text-slate-600">Cover letter</label>
                <textarea
                  value={coverLetter}
                  onChange={(e) => setCoverLetter(e.target.value)}
                  rows={6}
                  placeholder="Tell the recruiter why you're a fit for this role..."
                  className="w-full rounded-xl border border-slate-200 bg-slate-50 px-3 py-2.5 text-sm text-slate-800 outline-none focus:border-brand-400"
                />
              </div>
            </div>

            <button
              type="button"
              onClick={handleApply}
              disabled={submitting}
              className="mt-5 w-full rounded-xl bg-brand-600 px-4 py-3 text-sm font-semibold text-white transition hover:bg-brand-700 disabled:cursor-not-allowed disabled:opacity-70"
            >
              {submitting ? 'Submitting...' : 'Apply to this role'}
            </button>
          </div>
        </aside>
      </div>
    </div>
  );
};
