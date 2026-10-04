import React, { useEffect, useMemo, useState } from 'react';
import { ExternalLink, FileText, Search, Send, Users } from 'lucide-react';
import api, { API_BASE_URL } from '../../api/client';
import { useToast } from '../../context/ToastContext';

const statusLabels = {
  applied: 'Applied',
  screening: 'Under review',
  shortlisted: 'Shortlisted',
  interview: 'Interview',
  assessment: 'Assessment',
  offer: 'Offer made',
  hired: 'Hired',
  rejected: 'Not selected',
  withdrawn: 'Withdrawn',
};

const getCandidateName = (candidate) => {
  const user = candidate?.user || {};
  return `${user.first_name || ''} ${user.last_name || ''}`.trim() || user.email || 'Candidate';
};

const getResumeUrl = (application) => {
  const resume = application.resume || application.candidate?.resumes?.find((item) => item.is_default) || application.candidate?.resumes?.[0];
  const url = resume?.file_url_display || resume?.file_url || resume?.file;
  if (!url) return null;
  try {
    return new URL(url, API_BASE_URL).toString();
  } catch {
    return null;
  }
};

export const EmployerApplicants = () => {
  const { success, error } = useToast();
  const [applications, setApplications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [jobFilter, setJobFilter] = useState('all');
  const [inviteId, setInviteId] = useState(null);
  const [inviteMessage, setInviteMessage] = useState('');
  const [sendingId, setSendingId] = useState(null);

  useEffect(() => {
    const fetchApplications = async () => {
      try {
        const allApplications = [];
        let nextPage = '/api/applications/';
        while (nextPage) {
          const response = await api.get(nextPage);
          if (Array.isArray(response.data)) {
            allApplications.push(...response.data);
            nextPage = null;
          } else {
            allApplications.push(...(response.data?.results || []));
            nextPage = response.data?.next || null;
          }
        }
        setApplications(allApplications);
      } catch (err) {
        error(err.response?.data?.detail || 'Could not load your applicants.');
      } finally {
        setLoading(false);
      }
    };

    fetchApplications();
  }, [error]);

  const jobs = useMemo(() => {
    const uniqueJobs = new Map();
    applications.forEach((application) => {
      if (application.job) uniqueJobs.set(application.job.id, application.job.title);
    });
    return Array.from(uniqueJobs, ([id, title]) => ({ id, title }));
  }, [applications]);

  const filteredApplications = useMemo(() => {
    const query = search.trim().toLowerCase();
    return applications.filter((application) => {
      const candidate = application.candidate || {};
      const candidateName = getCandidateName(candidate).toLowerCase();
      const headline = (candidate.headline || '').toLowerCase();
      const jobTitle = (application.job?.title || '').toLowerCase();
      const skills = (candidate.skills || []).map((skill) => skill.skill_name || '').join(' ').toLowerCase();
      const matchesSearch = !query || [candidateName, headline, jobTitle, skills].some((value) => value.includes(query));
      const matchesJob = jobFilter === 'all' || String(application.job?.id) === jobFilter;
      return matchesSearch && matchesJob;
    });
  }, [applications, search, jobFilter]);

  const sendInterviewInvitation = async (application) => {
    try {
      setSendingId(application.id);
      await api.patch(`/api/applications/${application.id}/change_status/`, {
        status: 'interview',
        note: inviteMessage.trim(),
      });
      setApplications((current) => current.map((item) => (
        item.id === application.id ? { ...item, status: 'interview' } : item
      )));
      setInviteId(null);
      setInviteMessage('');
      success(`Interview invitation sent to ${getCandidateName(application.candidate)}.`);
    } catch (err) {
      error(err.response?.data?.detail || 'Could not send the interview invitation.');
    } finally {
      setSendingId(null);
    }
  };

  const interviewCount = applications.filter((application) => application.status === 'interview').length;

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
      <div className="flex flex-col gap-5 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.2em] text-brand-600">Recruiter workspace</p>
          <h1 className="mt-2 text-3xl font-black text-slate-900">Applicants</h1>
          <p className="mt-2 text-sm text-slate-600">Review candidates who applied to your company’s jobs and invite selected people to interview.</p>
        </div>
        <div className="flex gap-3 text-sm">
          <div className="rounded-xl border border-slate-200 bg-white px-4 py-3">
            <span className="block text-xs text-slate-500">Applicants</span>
            <strong className="mt-1 block text-xl text-slate-900">{applications.length}</strong>
          </div>
          <div className="rounded-xl border border-slate-200 bg-white px-4 py-3">
            <span className="block text-xs text-slate-500">Interview stage</span>
            <strong className="mt-1 block text-xl text-slate-900">{interviewCount}</strong>
          </div>
        </div>
      </div>

      <div className="mt-7 grid grid-cols-1 gap-3 sm:grid-cols-[1fr_260px]">
        <label className="flex items-center gap-2 rounded-xl border border-slate-200 bg-white px-3 py-2.5">
          <Search className="h-4 w-4 shrink-0 text-slate-400" />
          <input
            type="search"
            value={search}
            onChange={(event) => setSearch(event.target.value)}
            placeholder="Search candidate, skill, or role"
            className="w-full bg-transparent text-sm text-slate-800 outline-none"
          />
        </label>
        <select
          value={jobFilter}
          onChange={(event) => setJobFilter(event.target.value)}
          className="rounded-xl border border-slate-200 bg-white px-3 py-2.5 text-sm text-slate-700"
          aria-label="Filter applicants by job"
        >
          <option value="all">All jobs</option>
          {jobs.map((job) => <option key={job.id} value={job.id}>{job.title}</option>)}
        </select>
      </div>

      <div className="mt-5 space-y-3">
        {loading ? (
          <div className="rounded-2xl border border-slate-200 bg-white p-8 text-sm text-slate-500">Loading applicants...</div>
        ) : filteredApplications.length === 0 ? (
          <div className="rounded-2xl border border-slate-200 bg-white px-6 py-14 text-center">
            <Users className="mx-auto h-9 w-9 text-slate-300" />
            <h2 className="mt-3 font-semibold text-slate-900">No applicants found</h2>
            <p className="mt-1 text-sm text-slate-500">Applicants for your published jobs will appear here.</p>
          </div>
        ) : filteredApplications.map((application) => {
          const candidate = application.candidate || {};
          const candidateUser = candidate.user || {};
          const resumeUrl = getResumeUrl(application);
          const isInviting = inviteId === application.id;
          const alreadySelected = application.status === 'interview';
          const canInvite = !['interview', 'rejected', 'withdrawn', 'hired'].includes(application.status);

          return (
            <article key={application.id} className="rounded-2xl border border-slate-200 bg-white p-5 transition-shadow hover:shadow-md">
              <div className="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
                <div className="flex min-w-0 items-start gap-3">
                  <img
                    src={candidateUser.display_avatar || `https://api.dicebear.com/7.x/avataaars/svg?seed=${encodeURIComponent(candidateUser.email || candidate.id)}`}
                    alt=""
                    className="h-12 w-12 rounded-xl border border-slate-200 bg-slate-50 object-cover"
                  />
                  <div className="min-w-0">
                    <h2 className="font-bold text-slate-900">{getCandidateName(candidate)}</h2>
                    <p className="mt-0.5 text-sm text-slate-600">{candidate.headline || 'Candidate'} · {candidate.experience_years || 0} years experience</p>
                    <p className="mt-1 text-xs text-slate-500">Applied for <span className="font-semibold text-slate-700">{application.job?.title || 'Job'}</span></p>
                    <div className="mt-3 flex flex-wrap gap-1.5">
                      {(candidate.skills || []).slice(0, 6).map((skill) => (
                        <span key={skill.id} className="rounded-full bg-slate-100 px-2.5 py-1 text-[11px] font-medium text-slate-600">{skill.skill_name}</span>
                      ))}
                    </div>
                    {application.cover_letter && <p className="mt-3 max-w-3xl whitespace-pre-line text-sm leading-6 text-slate-600">{application.cover_letter}</p>}
                  </div>
                </div>

                <div className="flex shrink-0 flex-wrap items-center gap-2 lg:justify-end">
                  <span className="rounded-full bg-slate-100 px-3 py-1.5 text-xs font-semibold text-slate-700">{statusLabels[application.status] || application.status}</span>
                  {resumeUrl ? (
                    <a href={resumeUrl} target="_blank" rel="noreferrer" className="inline-flex items-center gap-1.5 rounded-lg border border-slate-200 px-3 py-2 text-xs font-semibold text-slate-700 hover:bg-slate-50">
                      <FileText className="h-3.5 w-3.5" /> View CV <ExternalLink className="h-3 w-3" />
                    </a>
                  ) : (
                    <span className="inline-flex items-center gap-1.5 rounded-lg border border-slate-200 px-3 py-2 text-xs text-slate-500"><FileText className="h-3.5 w-3.5" /> No CV attached</span>
                  )}
                  {canInvite && (
                    <button
                      type="button"
                      onClick={() => { setInviteId(isInviting ? null : application.id); setInviteMessage(''); }}
                      className="inline-flex items-center gap-1.5 rounded-lg bg-brand-600 px-3 py-2 text-xs font-semibold text-white hover:bg-brand-700"
                    >
                      <Send className="h-3.5 w-3.5" /> Invite to interview
                    </button>
                  )}
                </div>
              </div>

              {isInviting && (
                <div className="mt-4 border-t border-slate-100 pt-4">
                  <label className="mb-2 block text-xs font-semibold text-slate-700" htmlFor={`invite-message-${application.id}`}>Message to candidate (optional)</label>
                  <textarea
                    id={`invite-message-${application.id}`}
                    value={inviteMessage}
                    onChange={(event) => setInviteMessage(event.target.value)}
                    rows={3}
                    placeholder="Add a note about the interview. The candidate will receive it in their notifications."
                    className="w-full rounded-xl border border-slate-200 bg-slate-50 px-3 py-2.5 text-sm text-slate-800 outline-none focus:border-brand-400"
                  />
                  <div className="mt-3 flex justify-end gap-2">
                    <button type="button" onClick={() => setInviteId(null)} className="rounded-lg border border-slate-200 px-3 py-2 text-xs font-semibold text-slate-600">Cancel</button>
                    <button
                      type="button"
                      onClick={() => sendInterviewInvitation(application)}
                      disabled={sendingId === application.id}
                      className="rounded-lg bg-brand-600 px-3 py-2 text-xs font-semibold text-white hover:bg-brand-700 disabled:opacity-60"
                    >
                      {sendingId === application.id ? 'Sending...' : 'Send invitation'}
                    </button>
                  </div>
                </div>
              )}

              {alreadySelected && <p className="mt-4 border-t border-slate-100 pt-3 text-xs font-medium text-emerald-700">Interview invitation sent; candidate is in the interview stage.</p>}
            </article>
          );
        })}
      </div>
    </div>
  );
};
