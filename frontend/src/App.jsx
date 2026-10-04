import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { ToastProvider } from './context/ToastContext';
import { Navbar } from './components/common/Navbar';
import { Footer } from './components/common/Footer';
import { ProtectedRoute } from './components/common/ProtectedRoute';
import { Home } from './pages/Home';
import { JobSearch } from './pages/jobs/JobSearch';
import { JobDetail } from './pages/jobs/JobDetail';
import { PostJob } from './pages/jobs/PostJob';
import { Login } from './pages/auth/Login';
import { Register } from './pages/auth/Register';
import { ForgotPassword } from './pages/auth/ForgotPassword';
import { CandidateProfilePage } from './pages/candidates/CandidateProfile';
import { CandidateSavedJobs } from './pages/candidates/CandidateSavedJobs';

const stats = [
  { label: 'Open Roles', value: '128', tone: 'bg-brand-50 text-brand-700' },
  { label: 'Qualified Candidates', value: '3,480', tone: 'bg-emerald-50 text-emerald-700' },
  { label: 'Interviews Scheduled', value: '74', tone: 'bg-sky-50 text-sky-700' },
  { label: 'Offer Rate', value: '24%', tone: 'bg-violet-50 text-violet-700' },
];

const DashboardPage = ({ title, subtitle, role, items = [] }) => (
  <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
    <div className="mb-8">
      <p className="text-xs font-semibold uppercase tracking-[0.2em] text-brand-600">{role}</p>
      <h1 className="mt-2 text-3xl font-bold text-slate-900">{title}</h1>
      <p className="mt-2 text-sm text-slate-500">{subtitle}</p>
    </div>

    <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4 mb-8">
      {stats.map((stat) => (
        <div key={stat.label} className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
          <div className={`inline-flex rounded-xl px-2.5 py-1 text-xs font-semibold ${stat.tone}`}>
            {stat.label}
          </div>
          <p className="mt-4 text-3xl font-extrabold text-slate-900">{stat.value}</p>
        </div>
      ))}
    </div>

    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      {items.map((item) => (
        <div key={item.title} className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <div className="flex items-center justify-between">
            <h2 className="text-base font-semibold text-slate-900">{item.title}</h2>
            <span className={`inline-flex rounded-full px-2.5 py-1 text-[11px] font-semibold ${item.badgeClass}`}>
              {item.badge}
            </span>
          </div>
          <div className="mt-4 space-y-3">
            {item.rows.map((row) => (
              <div key={row.label} className="flex items-center justify-between rounded-xl bg-slate-50 px-3 py-2">
                <span className="text-xs text-slate-500">{row.label}</span>
                <span className="text-sm font-semibold text-slate-800">{row.value}</span>
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  </div>
);

const PricingPage = () => (
  <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
    <div className="text-center max-w-2xl mx-auto mb-10">
      <p className="text-xs font-semibold uppercase tracking-[0.3em] text-brand-600">Simple pricing</p>
      <h1 className="mt-3 text-4xl font-black text-slate-900">Scale your hiring without complexity</h1>
      <p className="mt-3 text-sm text-slate-600">Choose the plan that fits your recruitment needs, from startup hiring to enterprise ATS operations.</p>
    </div>

    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      {[
        { name: 'Starter', price: '$29', detail: 'For small teams hiring their first few roles.', features: ['3 active jobs', 'Basic screening', 'Email support'] },
        { name: 'Growth', price: '$99', detail: 'For teams ramping up hiring velocity.', features: ['Unlimited jobs', 'Advanced ATS', 'Interviews + analytics'], featured: true },
        { name: 'Enterprise', price: '$249', detail: 'For recruiting orgs with large-scale workflows.', features: ['Custom permissions', 'AI matching', 'Dedicated onboarding'] },
      ].map((plan) => (
        <div key={plan.name} className={`rounded-3xl border p-6 shadow-sm ${plan.featured ? 'border-brand-600 bg-brand-50/50' : 'border-slate-200 bg-white'}`}>
          <p className="text-xs font-semibold uppercase tracking-[0.2em] text-slate-500">{plan.name}</p>
          <div className="mt-4 flex items-end gap-2">
            <span className="text-4xl font-black text-slate-900">{plan.price}</span>
            <span className="text-sm text-slate-500">/month</span>
          </div>
          <p className="mt-3 text-sm text-slate-600">{plan.detail}</p>
          <ul className="mt-6 space-y-2 text-sm text-slate-700">
            {plan.features.map((feat) => (
              <li key={feat} className="flex items-center gap-2">
                <span className="inline-block h-2 w-2 rounded-full bg-brand-600" />
                {feat}
              </li>
            ))}
          </ul>
          <button className="mt-8 w-full rounded-xl bg-slate-900 px-4 py-2.5 text-sm font-semibold text-white hover:bg-slate-800">
            Choose {plan.name}
          </button>
        </div>
      ))}
    </div>
  </div>
);

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <ToastProvider>
          <div className="min-h-screen bg-slate-50 text-slate-900">
            <Navbar />
            <main className="min-h-[70vh]">
              <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/jobs" element={<JobSearch />} />
                <Route path="/jobs/:slug" element={<JobDetail />} />
                <Route path="/login" element={<Login />} />
                <Route path="/register" element={<Register />} />
                <Route path="/forgot-password" element={<ForgotPassword />} />
                <Route path="/pricing" element={<PricingPage />} />

                <Route
                  path="/candidate/profile"
                  element={
                    <ProtectedRoute allowedRoles={['candidate']}>
                      <CandidateProfilePage />
                    </ProtectedRoute>
                  }
                />

                <Route
                  path="/candidate/saved"
                  element={
                    <ProtectedRoute allowedRoles={['candidate']}>
                      <CandidateSavedJobs />
                    </ProtectedRoute>
                  }
                />

                <Route
                  path="/candidate/dashboard"
                  element={
                    <ProtectedRoute allowedRoles={['candidate']}>
                      <DashboardPage
                        role="Candidate"
                        title="Your career dashboard"
                        subtitle="Track applications, interviews, and saved roles in one place."
                        items={[
                          {
                            title: 'Applications',
                            badge: '8 active',
                            badgeClass: 'bg-blue-50 text-blue-700',
                            rows: [
                              { label: 'Submitted', value: '12' },
                              { label: 'Interviews', value: '3' },
                              { label: 'Shortlisted', value: '2' },
                            ],
                          },
                          {
                            title: 'Saved jobs',
                            badge: '14 saved',
                            badgeClass: 'bg-emerald-50 text-emerald-700',
                            rows: [
                              { label: 'Remote', value: '6' },
                              { label: 'Hybrid', value: '4' },
                              { label: 'On-site', value: '3' },
                            ],
                          },
                          {
                            title: 'Career pulse',
                            badge: 'Strong fit',
                            badgeClass: 'bg-violet-50 text-violet-700',
                            rows: [
                              { label: 'Profile score', value: '92%' },
                              { label: 'Interview readiness', value: 'High' },
                              { label: 'Skill matches', value: '18' },
                            ],
                          },
                        ]}
                      />
                    </ProtectedRoute>
                  }
                />

                <Route
                  path="/candidate/applications"
                  element={
                    <ProtectedRoute allowedRoles={['candidate']}>
                      <DashboardPage
                        role="Candidate"
                        title="Application tracker"
                        subtitle="Review statuses, upcoming interviews, and your latest recruiter updates."
                        items={[
                          {
                            title: 'Status overview',
                            badge: 'Live',
                            badgeClass: 'bg-emerald-50 text-emerald-700',
                            rows: [
                              { label: 'Applied', value: '8' },
                              { label: 'Screening', value: '2' },
                              { label: 'Offer', value: '1' },
                            ],
                          },
                          {
                            title: 'Interview timeline',
                            badge: 'Upcoming',
                            badgeClass: 'bg-yellow-50 text-yellow-700',
                            rows: [
                              { label: 'This week', value: '3' },
                              { label: 'Next 30 days', value: '6' },
                              { label: 'Assessments', value: '2' },
                            ],
                          },
                          {
                            title: 'Insights',
                            badge: 'Optimized',
                            badgeClass: 'bg-sky-50 text-sky-700',
                            rows: [
                              { label: 'Application response', value: '81%' },
                              { label: 'Avg response time', value: '5 days' },
                              { label: 'Match quality', value: '94%' },
                            ],
                          },
                        ]}
                      />
                    </ProtectedRoute>
                  }
                />

                <Route
                  path="/employer/dashboard"
                  element={
                    <ProtectedRoute allowedRoles={['employer']}>
                      <DashboardPage
                        role="Employer"
                        title="Hiring dashboard"
                        subtitle="Monitor role demand, pipeline health, and candidate performance across your hiring team."
                        items={[
                          {
                            title: 'Pipeline overview',
                            badge: 'Stable',
                            badgeClass: 'bg-emerald-50 text-emerald-700',
                            rows: [
                              { label: 'New applicants', value: '64' },
                              { label: 'Shortlisted', value: '18' },
                              { label: 'Interviews', value: '12' },
                            ],
                          },
                          {
                            title: 'Top roles',
                            badge: 'Priority',
                            badgeClass: 'bg-brand-50 text-brand-700',
                            rows: [
                              { label: 'Senior Frontend', value: '9' },
                              { label: 'Product Analyst', value: '6' },
                              { label: 'Data Engineer', value: '5' },
                            ],
                          },
                          {
                            title: 'Team efficiency',
                            badge: 'Fast',
                            badgeClass: 'bg-violet-50 text-violet-700',
                            rows: [
                              { label: 'Hiring velocity', value: '18 days' },
                              { label: 'Accepted offers', value: '6' },
                              { label: 'Avg. score', value: '86%' },
                            ],
                          },
                        ]}
                      />
                    </ProtectedRoute>
                  }
                />

                <Route
                  path="/employer/jobs"
                  element={
                    <ProtectedRoute allowedRoles={['employer']}>
                      <PostJob />
                    </ProtectedRoute>
                  }
                />

                <Route
                  path="/employer/post-job"
                  element={
                    <ProtectedRoute allowedRoles={['employer']}>
                      <PostJob />
                    </ProtectedRoute>
                  }
                />

                <Route
                  path="/employer/ats"
                  element={
                    <ProtectedRoute allowedRoles={['employer']}>
                      <DashboardPage
                        role="Employer"
                        title="Kanban pipeline"
                        subtitle="Visualize candidates by stage, review team notes, and move talent quickly through hiring stages."
                        items={[
                          {
                            title: 'Candidate flow',
                            badge: 'Healthy',
                            badgeClass: 'bg-emerald-50 text-emerald-700',
                            rows: [
                              { label: 'Applied', value: '114' },
                              { label: 'Screening', value: '37' },
                              { label: 'Interview', value: '21' },
                            ],
                          },
                          {
                            title: 'Team workload',
                            badge: 'Balanced',
                            badgeClass: 'bg-violet-50 text-violet-700',
                            rows: [
                              { label: 'Reviewers online', value: '7' },
                              { label: 'Avg. cycle time', value: '4.2d' },
                              { label: 'SLAs met', value: '92%' },
                            ],
                          },
                          {
                            title: 'Hiring notes',
                            badge: 'Updated',
                            badgeClass: 'bg-sky-50 text-sky-700',
                            rows: [
                              { label: 'Comments this week', value: '61' },
                              { label: 'Follow-ups due', value: '8' },
                              { label: 'Feedback loops', value: '14' },
                            ],
                          },
                        ]}
                      />
                    </ProtectedRoute>
                  }
                />

                <Route
                  path="/employer/candidates"
                  element={
                    <ProtectedRoute allowedRoles={['employer']}>
                      <DashboardPage
                        role="Employer"
                        title="Talent search"
                        subtitle="Search, shortlist, and engage the best-fit candidates for your upcoming hires."
                        items={[
                          {
                            title: 'Talent pool',
                            badge: '2,418',
                            badgeClass: 'bg-brand-50 text-brand-700',
                            rows: [
                              { label: 'Active profiles', value: '1,252' },
                              { label: 'Verified', value: '842' },
                              { label: 'Open to work', value: '618' },
                            ],
                          },
                          {
                            title: 'Top skills',
                            badge: 'Popular',
                            badgeClass: 'bg-emerald-50 text-emerald-700',
                            rows: [
                              { label: 'React', value: '291' },
                              { label: 'Python', value: '216' },
                              { label: 'Data', value: '184' },
                            ],
                          },
                          {
                            title: 'Engagement',
                            badge: 'Responsive',
                            badgeClass: 'bg-violet-50 text-violet-700',
                            rows: [
                              { label: 'Responses', value: '73%' },
                              { label: 'Avg. response time', value: '2h' },
                              { label: 'Saved searches', value: '17' },
                            ],
                          },
                        ]}
                      />
                    </ProtectedRoute>
                  }
                />

                <Route
                  path="/admin/dashboard"
                  element={
                    <ProtectedRoute allowedRoles={['admin']}>
                      <DashboardPage
                        role="Admin"
                        title="Platform overview"
                        subtitle="Keep the system secure, healthy, and operating at scale for all users."
                        items={[
                          {
                            title: 'Operations',
                            badge: 'Healthy',
                            badgeClass: 'bg-emerald-50 text-emerald-700',
                            rows: [
                              { label: 'API uptime', value: '99.96%' },
                              { label: 'Transactions', value: '24.1k' },
                              { label: 'Failed jobs', value: '3' },
                            ],
                          },
                          {
                            title: 'Moderation queue',
                            badge: '12 pending',
                            badgeClass: 'bg-amber-50 text-amber-700',
                            rows: [
                              { label: 'Profiles', value: '6' },
                              { label: 'Employer checks', value: '4' },
                              { label: 'Jobs flagged', value: '2' },
                            ],
                          },
                          {
                            title: 'Revenue health',
                            badge: 'Strong',
                            badgeClass: 'bg-brand-50 text-brand-700',
                            rows: [
                              { label: 'MRR', value: '$48.5k' },
                              { label: 'Conversion', value: '7.1%' },
                              { label: 'Churn', value: '1.2%' },
                            ],
                          },
                        ]}
                      />
                    </ProtectedRoute>
                  }
                />

                <Route
                  path="/admin/moderation"
                  element={
                    <ProtectedRoute allowedRoles={['admin']}>
                      <DashboardPage
                        role="Admin"
                        title="Moderation center"
                        subtitle="Review reports, inspect compliance flags, and keep the community safe."
                        items={[
                          {
                            title: 'Queue',
                            badge: 'Review',
                            badgeClass: 'bg-amber-50 text-amber-700',
                            rows: [
                              { label: 'Profiles', value: '9' },
                              { label: 'Jobs', value: '5' },
                              { label: 'Messages', value: '7' },
                            ],
                          },
                          {
                            title: 'Compliance',
                            badge: 'Updated',
                            badgeClass: 'bg-emerald-50 text-emerald-700',
                            rows: [
                              { label: 'Verified employers', value: '96%' },
                              { label: 'KYC checks', value: '1,242' },
                              { label: 'Flagged items', value: '11' },
                            ],
                          },
                          {
                            title: 'Action rate',
                            badge: 'Fast',
                            badgeClass: 'bg-sky-50 text-sky-700',
                            rows: [
                              { label: 'Resolved today', value: '27' },
                              { label: 'Avg resolution', value: '5h' },
                              { label: 'Escalations', value: '2' },
                            ],
                          },
                        ]}
                      />
                    </ProtectedRoute>
                  }
                />

                <Route
                  path="/admin/verifications"
                  element={
                    <ProtectedRoute allowedRoles={['admin']}>
                      <DashboardPage
                        role="Admin"
                        title="Verification hub"
                        subtitle="Validate employer identity and confirm candidate trust markers to keep platform quality high."
                        items={[
                          {
                            title: 'Identity checks',
                            badge: '98%',
                            badgeClass: 'bg-emerald-50 text-emerald-700',
                            rows: [
                              { label: 'Passed', value: '1,482' },
                              { label: 'Pending', value: '41' },
                              { label: 'Expired', value: '17' },
                            ],
                          },
                          {
                            title: 'Employer trust',
                            badge: 'Stable',
                            badgeClass: 'bg-brand-50 text-brand-700',
                            rows: [
                              { label: 'Verified orgs', value: '218' },
                              { label: 'Domain checks', value: '98%' },
                              { label: 'Reviews', value: '31' },
                            ],
                          },
                          {
                            title: 'Candidate trust',
                            badge: 'Strong',
                            badgeClass: 'bg-violet-50 text-violet-700',
                            rows: [
                              { label: 'Profiles verified', value: '892' },
                              { label: 'Documents checked', value: '254' },
                              { label: 'Verification SLA', value: '24h' },
                            ],
                          },
                        ]}
                      />
                    </ProtectedRoute>
                  }
                />

                <Route path="*" element={<Navigate to="/" replace />} />
              </Routes>
            </main>
            <Footer />
          </div>
        </ToastProvider>
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;
