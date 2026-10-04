import React, { useEffect, useMemo, useState } from 'react';
import { Link } from 'react-router-dom';
import {
  Award,
  Briefcase,
  Building2,
  CheckCircle2,
  Clock3,
  Download,
  ExternalLink,
  FileText,
  Globe,
  GraduationCap,
  MapPin,
  Mail,
  PencilLine,
  Sparkles,
  Star,
  Target,
  Upload,
} from 'lucide-react';
import api, { API_BASE_URL } from '../../api/client';
import { useAuth } from '../../context/AuthContext';
import { useToast } from '../../context/ToastContext';

const formatMoney = (value) => {
  const num = Number(value || 0);
  if (!num) return 'Open to discussion';
  return `$${num.toLocaleString()}`;
};

const getResumeUrl = (resume) => {
  const url = resume?.file_url_display || resume?.file_url || resume?.file;
  if (!url) return '';
  try {
    return new URL(url, API_BASE_URL).toString();
  } catch {
    return '';
  }
};

export const CandidateProfilePage = () => {
  const { user } = useAuth();
  const { success, error } = useToast();
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [uploadingResume, setUploadingResume] = useState(false);

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const res = await api.get('/api/candidates/profiles/me/');
        setProfile(res.data || null);
      } catch (err) {
        console.error('Profile fetch failed:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchProfile();
  }, []);

  const profileStrength = useMemo(() => profile?.profile_strength ?? 0, [profile]);

  if (loading) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-10">
        <div className="animate-pulse space-y-6">
          <div className="h-52 rounded-3xl bg-slate-200" />
          <div className="grid md:grid-cols-3 gap-6">
            <div className="h-48 rounded-3xl bg-slate-200" />
            <div className="h-48 rounded-3xl bg-slate-200" />
            <div className="h-48 rounded-3xl bg-slate-200" />
          </div>
        </div>
      </div>
    );
  }

  const candidate = profile?.user || user || {};
  const headline = profile?.headline || 'Full Stack Software Engineer';
  const skills = profile?.skills || [];
  const experience = profile?.experiences || [];
  const education = profile?.educations || [];
  const projects = profile?.projects || [];
  const certifications = profile?.certifications || [];
  const resumes = profile?.resumes || [];
  const defaultResume = resumes.find((resume) => resume.is_default) || resumes[0];

  const refreshProfile = async () => {
    const response = await api.get('/api/candidates/profiles/me/');
    setProfile(response.data || null);
  };

  const handleResumeUpload = async (event) => {
    const file = event.target.files?.[0];
    if (!file) return;

    const extension = file.name.split('.').pop()?.toLowerCase();
    if (!['pdf', 'doc', 'docx'].includes(extension)) {
      error('Upload a PDF, DOC, or DOCX file.');
      event.target.value = '';
      return;
    }
    if (file.size > 10 * 1024 * 1024) {
      error('CV files must be 10 MB or smaller.');
      event.target.value = '';
      return;
    }

    const formData = new FormData();
    formData.append('title', file.name.replace(/\.[^.]+$/, '') || 'My CV');
    formData.append('file', file);

    try {
      setUploadingResume(true);
      await api.post('/api/candidates/resumes/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      await refreshProfile();
      success('Your CV has been uploaded.');
    } catch (err) {
      const detail = err.response?.data?.file?.[0] || err.response?.data?.detail;
      error(detail || 'Could not upload your CV.');
    } finally {
      setUploadingResume(false);
      event.target.value = '';
    }
  };

  const setDefaultResume = async (resumeId) => {
    try {
      await api.post(`/api/candidates/resumes/${resumeId}/set_default/`);
      await refreshProfile();
      success('Default CV updated.');
    } catch (err) {
      error('Could not update your default CV.');
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
      <div className="rounded-[32px] border border-slate-200 bg-white shadow-sm overflow-hidden">
        <div className="bg-gradient-to-r from-brand-50 via-white to-sky-50 px-6 py-6 md:px-8">
          <div className="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-6">
            <div className="flex items-center gap-5">
              <img
                src={candidate.display_avatar || candidate.avatar_url || `https://api.dicebear.com/7.x/avataaars/svg?seed=${candidate.email || 'candidate'}`}
                alt={candidate.first_name || 'Candidate'}
                className="h-20 w-20 rounded-2xl object-cover ring-4 ring-white shadow-lg"
              />
              <div>
                <p className="text-xs font-semibold uppercase tracking-[0.2em] text-brand-600">Candidate profile</p>
                <h1 className="mt-2 text-3xl font-black text-slate-900">
                  {candidate.first_name || 'Candidate'} {candidate.last_name || ''}
                </h1>
                <p className="mt-1 text-base text-slate-600">{headline}</p>
                <div className="mt-3 flex flex-wrap items-center gap-3 text-xs text-slate-500">
                  <span className="inline-flex items-center gap-1.5"><MapPin className="w-3.5 h-3.5" />{profile?.preferred_location || 'Remote'}</span>
                  <span className="inline-flex items-center gap-1.5"><Briefcase className="w-3.5 h-3.5" />{profile?.preferred_employment_type || 'Full-time'}</span>
                  <span className="inline-flex items-center gap-1.5"><Clock3 className="w-3.5 h-3.5" />{profile?.experience_years || 0} years experience</span>
                </div>
              </div>
            </div>

            <div className="flex items-center gap-3">
              <Link to="/candidate/applications" className="inline-flex items-center gap-2 rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-sm font-semibold text-slate-700 hover:bg-slate-50">
                <PencilLine className="w-4 h-4" />
                Edit profile
              </Link>
              <label className="inline-flex cursor-pointer items-center gap-2 rounded-xl bg-brand-600 px-4 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-brand-700">
                <Upload className="w-4 h-4" />
                {uploadingResume ? 'Uploading...' : 'Upload CV'}
                <input type="file" accept=".pdf,.doc,.docx" className="sr-only" onChange={handleResumeUpload} disabled={uploadingResume} />
              </label>
              {defaultResume && (
                <a
                  href={getResumeUrl(defaultResume)}
                  target="_blank"
                  rel="noreferrer"
                  className="inline-flex items-center gap-2 rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-sm font-semibold text-slate-700 hover:bg-slate-50"
                >
                  <Download className="w-4 h-4" />
                  View CV
                </a>
              )}
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 xl:grid-cols-[1.3fr_0.7fr] gap-6 p-6 md:p-8">
          <div className="space-y-6">
            <section className="rounded-3xl border border-slate-200 bg-slate-50 p-5">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Target className="w-4 h-4 text-brand-600" />
                  <h2 className="text-lg font-bold text-slate-900">Profile strength</h2>
                </div>
                <span className="text-sm font-bold text-brand-700">{profileStrength}%</span>
              </div>
              <div className="mt-4 h-2.5 w-full rounded-full bg-slate-200">
                <div className="h-2.5 rounded-full bg-gradient-to-r from-brand-600 to-sky-500" style={{ width: `${profileStrength}%` }} />
              </div>
              <div className="mt-4 grid gap-2 text-xs text-slate-600">
                {profile?.profile_strength_details?.suggestions?.length ? (
                  profile.profile_strength_details.suggestions.slice(0, 4).map((item) => (
                    <div key={item} className="flex items-center gap-2">
                      <CheckCircle2 className="h-3.5 w-3.5 text-emerald-600" />
                      <span>{item}</span>
                    </div>
                  ))
                ) : (
                  <div className="flex items-center gap-2"><CheckCircle2 className="h-3.5 w-3.5 text-emerald-600" /><span>Your profile is in great shape.</span></div>
                )}
              </div>
            </section>

            <section className="rounded-3xl border border-slate-200 bg-white p-5">
              <div className="flex items-center gap-2 mb-4">
                <Sparkles className="w-4 h-4 text-brand-600" />
                <h2 className="text-lg font-bold text-slate-900">Core skills</h2>
              </div>
              <div className="flex flex-wrap gap-2">
                {skills.length ? (
                  skills.map((skill) => (
                    <span key={skill.id || skill.skill_name} className="rounded-full border border-brand-200 bg-brand-50 px-3 py-1.5 text-xs font-semibold text-brand-700">
                      {skill.skill_name || skill.skill?.name}
                    </span>
                  ))
                ) : (
                  <span className="text-sm text-slate-500">No skills added yet.</span>
                )}
              </div>
            </section>

            <section className="rounded-3xl border border-slate-200 bg-white p-5">
              <div className="flex items-center gap-2 mb-4">
                <Briefcase className="w-4 h-4 text-brand-600" />
                <h2 className="text-lg font-bold text-slate-900">Experience</h2>
              </div>
              <div className="space-y-4">
                {experience.length ? (
                  experience.map((job) => (
                    <div key={job.id} className="rounded-2xl bg-slate-50 p-4 border border-slate-200">
                      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2">
                        <div>
                          <p className="text-base font-bold text-slate-900">{job.job_title}</p>
                          <p className="text-sm text-slate-600">{job.company_name}</p>
                        </div>
                        <span className="inline-flex items-center rounded-full bg-white px-2.5 py-1 text-[11px] font-semibold text-slate-600 border border-slate-200">
                          {job.is_current ? 'Current role' : 'Previous role'}
                        </span>
                      </div>
                      <p className="mt-2 text-xs text-slate-500">
                        {job.location || 'Remote'} · {job.workplace_type || 'Hybrid'}
                      </p>
                      <ul className="mt-3 space-y-1.5 text-sm text-slate-600">
                        {(job.responsibilities || []).slice(0, 3).map((item) => (
                          <li key={item} className="flex items-start gap-2">
                            <span className="mt-1 h-1.5 w-1.5 rounded-full bg-brand-500" />
                            <span>{item}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  ))
                ) : (
                  <p className="text-sm text-slate-500">Experience details have not been added yet.</p>
                )}
              </div>
            </section>

            <section className="rounded-3xl border border-slate-200 bg-white p-5">
              <div className="flex items-center gap-2 mb-4">
                <GraduationCap className="w-4 h-4 text-brand-600" />
                <h2 className="text-lg font-bold text-slate-900">Education</h2>
              </div>
              <div className="space-y-3">
                {education.length ? (
                  education.map((item) => (
                    <div key={item.id} className="rounded-2xl bg-slate-50 p-4 border border-slate-200">
                      <p className="font-semibold text-slate-900">{item.degree}</p>
                      <p className="text-sm text-slate-600">{item.institution}</p>
                      <p className="mt-1 text-xs text-slate-500">{item.field_of_study}</p>
                    </div>
                  ))
                ) : (
                  <p className="text-sm text-slate-500">No education details added.</p>
                )}
              </div>
            </section>
          </div>

          <div className="space-y-6">
            <section className="rounded-3xl border border-slate-200 bg-white p-5">
              <div className="flex items-center gap-2 mb-4">
                <Star className="w-4 h-4 text-brand-600" />
                <h2 className="text-lg font-bold text-slate-900">Overview</h2>
              </div>
              <div className="space-y-3 text-sm text-slate-600">
                <div className="flex items-center justify-between rounded-xl bg-slate-50 px-3 py-2.5">
                  <span>Expected salary</span>
                  <strong className="text-slate-900">{formatMoney(profile?.expected_salary)}</strong>
                </div>
                <div className="flex items-center justify-between rounded-xl bg-slate-50 px-3 py-2.5">
                  <span>Open to work</span>
                  <strong className="text-slate-900">{profile?.is_open_to_work ? 'Yes' : 'No'}</strong>
                </div>
                <div className="flex items-center justify-between rounded-xl bg-slate-50 px-3 py-2.5">
                  <span>Portfolio</span>
                  <strong className="text-slate-900">{profile?.portfolio_url ? 'Linked' : 'Not set'}</strong>
                </div>
                <div className="flex items-center justify-between rounded-xl bg-slate-50 px-3 py-2.5">
                  <span>Resumes</span>
                  <strong className="text-slate-900">{resumes.length}</strong>
                </div>
              </div>
            </section>

            <section className="rounded-3xl border border-slate-200 bg-white p-5">
              <div className="flex items-center gap-2 mb-4">
                <Mail className="w-4 h-4 text-brand-600" />
                <h2 className="text-lg font-bold text-slate-900">Contact</h2>
              </div>
              <div className="space-y-3 text-sm text-slate-600">
                <div className="flex items-center justify-between rounded-xl bg-slate-50 px-3 py-2.5">
                  <span>Email</span>
                  <span className="font-medium text-slate-900">{candidate.email}</span>
                </div>
                <div className="flex items-center justify-between rounded-xl bg-slate-50 px-3 py-2.5">
                  <span>GitHub</span>
                  <a href={profile?.github_url || '#'} target="_blank" rel="noreferrer" className="inline-flex items-center gap-1 text-brand-700">
                    {profile?.github_url ? <Globe className="w-3.5 h-3.5" /> : 'Not set'}
                    {profile?.github_url ? 'View' : ''}
                  </a>
                </div>
                <div className="flex items-center justify-between rounded-xl bg-slate-50 px-3 py-2.5">
                  <span>LinkedIn</span>
                  <a href={profile?.linkedin_url || '#'} target="_blank" rel="noreferrer" className="inline-flex items-center gap-1 text-brand-700">
                    {profile?.linkedin_url ? <ExternalLink className="w-3.5 h-3.5" /> : 'Not set'}
                    {profile?.linkedin_url ? 'Profile' : ''}
                  </a>
                </div>
              </div>
            </section>

            <section className="rounded-3xl border border-slate-200 bg-white p-5">
              <div className="flex items-center gap-2 mb-4">
                <FileText className="w-4 h-4 text-brand-600" />
                <h2 className="text-lg font-bold text-slate-900">My CVs</h2>
              </div>
              {resumes.length ? (
                <div className="space-y-2">
                  {resumes.map((resume) => (
                    <div key={resume.id} className="flex items-center justify-between gap-3 rounded-xl bg-slate-50 px-3 py-2.5">
                      <div className="min-w-0">
                        <p className="truncate text-sm font-semibold text-slate-800">{resume.title}</p>
                        <p className="text-xs text-slate-500">{resume.file_extension?.toUpperCase()} · {resume.file_size_kb} KB{resume.is_default ? ' · Default' : ''}</p>
                      </div>
                      {!resume.is_default && (
                        <button type="button" onClick={() => setDefaultResume(resume.id)} className="shrink-0 text-xs font-semibold text-brand-700 hover:text-brand-900">Set default</button>
                      )}
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-sm text-slate-500">Upload a PDF, DOC, or DOCX CV to share it with recruiters when you apply.</p>
              )}
            </section>

            <section className="rounded-3xl border border-slate-200 bg-white p-5">
              <div className="flex items-center gap-2 mb-4">
                <Award className="w-4 h-4 text-brand-600" />
                <h2 className="text-lg font-bold text-slate-900">Certifications</h2>
              </div>
              {certifications.length ? (
                <div className="space-y-3">
                  {certifications.map((item) => (
                    <div key={item.id} className="rounded-2xl bg-slate-50 p-3 border border-slate-200">
                      <p className="font-semibold text-slate-900">{item.name}</p>
                      <p className="text-xs text-slate-500">{item.issuing_organization}</p>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-sm text-slate-500">No certifications added yet.</p>
              )}
            </section>

            <section className="rounded-3xl border border-slate-200 bg-white p-5">
              <div className="flex items-center gap-2 mb-4">
                <Building2 className="w-4 h-4 text-brand-600" />
                <h2 className="text-lg font-bold text-slate-900">Projects</h2>
              </div>
              {projects.length ? (
                <div className="space-y-3">
                  {projects.map((item) => (
                    <div key={item.id} className="rounded-2xl bg-slate-50 p-3 border border-slate-200">
                      <p className="font-semibold text-slate-900">{item.title}</p>
                      <p className="mt-1 text-xs text-slate-600">{item.description}</p>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-sm text-slate-500">Project portfolio is empty.</p>
              )}
            </section>
          </div>
        </div>
      </div>
    </div>
  );
};
