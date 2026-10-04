import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Briefcase, Building2, CheckCircle2 } from 'lucide-react';
import api from '../../api/client';
import { useAuth } from '../../context/AuthContext';
import { useToast } from '../../context/ToastContext';

const initialForm = {
  title: '',
  department: 'Engineering',
  category: '',
  employment_type: 'full_time',
  workplace_type: 'remote',
  location: 'Remote',
  min_salary: '100000',
  max_salary: '150000',
  experience_level: 'mid',
  education_level: "Bachelor's Degree in Computer Science or related field",
  description: '',
  responsibilities: '',
  requirements: '',
  benefits: '',
  vacancies: '1',
  deadline: '',
  skills_data: 'React, JavaScript, Product Thinking',
  status: 'published',
};

export const PostJob = () => {
  const navigate = useNavigate();
  const { user, isAuthenticated, isEmployer } = useAuth();
  const { success, error, info } = useToast();
  const [form, setForm] = useState(initialForm);
  const [categories, setCategories] = useState([]);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const res = await api.get('/api/jobs/categories/');
        const list = res.data?.results || res.data || [];
        setCategories(list);
        if (list[0]) setForm((prev) => ({ ...prev, category: String(list[0].id) }));
      } catch (err) {
        console.error(err);
      }
    };

    fetchCategories();
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!isAuthenticated) {
      info('Please sign in as an employer to post a role.');
      navigate('/login');
      return;
    }

    if (!isEmployer) {
      info('Only employers can post jobs on this platform.');
      return;
    }

    try {
      setSubmitting(true);

      const payload = {
        ...form,
        category: Number(form.category),
        min_salary: form.min_salary ? Number(form.min_salary) : null,
        max_salary: form.max_salary ? Number(form.max_salary) : null,
        vacancies: Number(form.vacancies || 1),
        responsibilities: form.responsibilities
          .split('\n')
          .map((line) => line.trim())
          .filter(Boolean),
        requirements: form.requirements
          .split('\n')
          .map((line) => line.trim())
          .filter(Boolean),
        benefits: form.benefits
          .split(',')
          .map((item) => item.trim())
          .filter(Boolean),
        skills_data: form.skills_data
          .split(',')
          .map((skill) => skill.trim())
          .filter(Boolean),
        deadline: form.deadline ? new Date(form.deadline).toISOString() : null,
      };

      await api.post('/api/jobs/listings/', payload);
      success('Your job has been posted successfully.');
      navigate('/employer/dashboard');
    } catch (err) {
      const message =
        err.response?.data?.detail ||
        err.response?.data?.non_field_errors?.[0] ||
        Object.values(err.response?.data || {})?.flat()?.[0] ||
        'Unable to post the job right now.';
      error(message);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-6 flex items-center justify-between gap-3">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.2em] text-brand-600">Recruiter workspace</p>
          <h1 className="mt-2 text-3xl font-black text-slate-900">Post a new job</h1>
        </div>
        <div className="hidden sm:flex items-center gap-2 rounded-full bg-emerald-50 px-3 py-1.5 text-xs font-semibold text-emerald-700 border border-emerald-200">
          <CheckCircle2 className="h-4 w-4" />
          Live hiring
        </div>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <div className="md:col-span-2 flex items-center gap-3 rounded-2xl bg-brand-50 px-4 py-3 border border-brand-100 text-sm text-brand-800">
            <Briefcase className="h-5 w-5" />
            Posting as <span className="font-bold">{user?.company_name || 'Your company'}</span>
          </div>

          <div className="md:col-span-2">
            <label className="mb-2 block text-xs font-semibold uppercase tracking-wide text-slate-600">Job title</label>
            <input name="title" value={form.title} onChange={handleChange} required className="w-full rounded-xl border border-slate-200 bg-slate-50 px-3 py-2.5 text-sm text-slate-800 outline-none focus:border-brand-400" placeholder="Senior Product Designer" />
          </div>

          <div>
            <label className="mb-2 block text-xs font-semibold uppercase tracking-wide text-slate-600">Department</label>
            <input name="department" value={form.department} onChange={handleChange} className="w-full rounded-xl border border-slate-200 bg-slate-50 px-3 py-2.5 text-sm text-slate-800 outline-none focus:border-brand-400" />
          </div>

          <div>
            <label className="mb-2 block text-xs font-semibold uppercase tracking-wide text-slate-600">Category</label>
            <select name="category" value={form.category} onChange={handleChange} className="w-full rounded-xl border border-slate-200 bg-slate-50 px-3 py-2.5 text-sm text-slate-800 outline-none focus:border-brand-400">
              {categories.map((category) => (
                <option key={category.id} value={category.id}>{category.name}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="mb-2 block text-xs font-semibold uppercase tracking-wide text-slate-600">Employment type</label>
            <select name="employment_type" value={form.employment_type} onChange={handleChange} className="w-full rounded-xl border border-slate-200 bg-slate-50 px-3 py-2.5 text-sm text-slate-800 outline-none focus:border-brand-400">
              <option value="full_time">Full-time</option>
              <option value="part_time">Part-time</option>
              <option value="contract">Contract</option>
              <option value="internship">Internship</option>
              <option value="remote">Remote</option>
            </select>
          </div>

          <div>
            <label className="mb-2 block text-xs font-semibold uppercase tracking-wide text-slate-600">Workplace type</label>
            <select name="workplace_type" value={form.workplace_type} onChange={handleChange} className="w-full rounded-xl border border-slate-200 bg-slate-50 px-3 py-2.5 text-sm text-slate-800 outline-none focus:border-brand-400">
              <option value="on_site">On-site</option>
              <option value="hybrid">Hybrid</option>
              <option value="remote">Remote</option>
            </select>
          </div>

          <div>
            <label className="mb-2 block text-xs font-semibold uppercase tracking-wide text-slate-600">Location</label>
            <input name="location" value={form.location} onChange={handleChange} className="w-full rounded-xl border border-slate-200 bg-slate-50 px-3 py-2.5 text-sm text-slate-800 outline-none focus:border-brand-400" />
          </div>

          <div>
            <label className="mb-2 block text-xs font-semibold uppercase tracking-wide text-slate-600">Vacancies</label>
            <input type="number" min="1" name="vacancies" value={form.vacancies} onChange={handleChange} className="w-full rounded-xl border border-slate-200 bg-slate-50 px-3 py-2.5 text-sm text-slate-800 outline-none focus:border-brand-400" />
          </div>

          <div>
            <label className="mb-2 block text-xs font-semibold uppercase tracking-wide text-slate-600">Min salary</label>
            <input type="number" name="min_salary" value={form.min_salary} onChange={handleChange} className="w-full rounded-xl border border-slate-200 bg-slate-50 px-3 py-2.5 text-sm text-slate-800 outline-none focus:border-brand-400" />
          </div>

          <div>
            <label className="mb-2 block text-xs font-semibold uppercase tracking-wide text-slate-600">Max salary</label>
            <input type="number" name="max_salary" value={form.max_salary} onChange={handleChange} className="w-full rounded-xl border border-slate-200 bg-slate-50 px-3 py-2.5 text-sm text-slate-800 outline-none focus:border-brand-400" />
          </div>

          <div>
            <label className="mb-2 block text-xs font-semibold uppercase tracking-wide text-slate-600">Experience level</label>
            <select name="experience_level" value={form.experience_level} onChange={handleChange} className="w-full rounded-xl border border-slate-200 bg-slate-50 px-3 py-2.5 text-sm text-slate-800 outline-none focus:border-brand-400">
              <option value="entry">Entry</option>
              <option value="junior">Junior</option>
              <option value="mid">Mid</option>
              <option value="senior">Senior</option>
              <option value="lead">Lead</option>
              <option value="executive">Executive</option>
            </select>
          </div>

          <div>
            <label className="mb-2 block text-xs font-semibold uppercase tracking-wide text-slate-600">Application deadline</label>
            <input type="date" name="deadline" value={form.deadline} onChange={handleChange} className="w-full rounded-xl border border-slate-200 bg-slate-50 px-3 py-2.5 text-sm text-slate-800 outline-none focus:border-brand-400" />
          </div>

          <div className="md:col-span-2">
            <label className="mb-2 block text-xs font-semibold uppercase tracking-wide text-slate-600">Role description</label>
            <textarea name="description" value={form.description} onChange={handleChange} rows={5} required className="w-full rounded-xl border border-slate-200 bg-slate-50 px-3 py-2.5 text-sm text-slate-800 outline-none focus:border-brand-400" placeholder="Describe the role, business context, and what success looks like..." />
          </div>

          <div>
            <label className="mb-2 block text-xs font-semibold uppercase tracking-wide text-slate-600">Responsibilities (one per line)</label>
            <textarea name="responsibilities" value={form.responsibilities} onChange={handleChange} rows={5} className="w-full rounded-xl border border-slate-200 bg-slate-50 px-3 py-2.5 text-sm text-slate-800 outline-none focus:border-brand-400" placeholder="Lead product discovery&#10;Define roadmap" />
          </div>

          <div>
            <label className="mb-2 block text-xs font-semibold uppercase tracking-wide text-slate-600">Requirements (one per line)</label>
            <textarea name="requirements" value={form.requirements} onChange={handleChange} rows={5} className="w-full rounded-xl border border-slate-200 bg-slate-50 px-3 py-2.5 text-sm text-slate-800 outline-none focus:border-brand-400" placeholder="3+ years of experience&#10;Strong communication" />
          </div>

          <div className="md:col-span-2">
            <label className="mb-2 block text-xs font-semibold uppercase tracking-wide text-slate-600">Benefits (comma-separated)</label>
            <input name="benefits" value={form.benefits} onChange={handleChange} className="w-full rounded-xl border border-slate-200 bg-slate-50 px-3 py-2.5 text-sm text-slate-800 outline-none focus:border-brand-400" placeholder="Healthcare, remote flexibility, annual bonus" />
          </div>

          <div className="md:col-span-2">
            <label className="mb-2 block text-xs font-semibold uppercase tracking-wide text-slate-600">Key skills (comma-separated)</label>
            <input name="skills_data" value={form.skills_data} onChange={handleChange} className="w-full rounded-xl border border-slate-200 bg-slate-50 px-3 py-2.5 text-sm text-slate-800 outline-none focus:border-brand-400" placeholder="React, Product strategy, UX" />
          </div>

          <div className="md:col-span-2">
            <label className="mb-2 block text-xs font-semibold uppercase tracking-wide text-slate-600">Education requirement</label>
            <input name="education_level" value={form.education_level} onChange={handleChange} className="w-full rounded-xl border border-slate-200 bg-slate-50 px-3 py-2.5 text-sm text-slate-800 outline-none focus:border-brand-400" />
          </div>
        </div>

        <div className="flex items-center justify-end gap-3 rounded-3xl border border-slate-200 bg-white p-4 shadow-sm">
          <button type="button" onClick={() => navigate('/employer/dashboard')} className="rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-sm font-semibold text-slate-700 hover:bg-slate-50">
            Cancel
          </button>
          <button type="submit" disabled={submitting} className="rounded-xl bg-brand-600 px-5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-brand-700 disabled:opacity-70">
            {submitting ? 'Publishing...' : 'Publish job'}
          </button>
        </div>
      </form>
    </div>
  );
};
