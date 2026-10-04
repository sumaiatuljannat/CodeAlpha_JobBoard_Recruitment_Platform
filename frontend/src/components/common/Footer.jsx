import React from 'react';
import { Link } from 'react-router-dom';
import { Briefcase, ShieldCheck, Globe, Sparkles, Building2 } from 'lucide-react';

export const Footer = () => {
  return (
    <footer className="bg-slate-900 text-slate-400 text-xs border-t border-slate-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Brand */}
          <div className="space-y-4">
            <div className="flex items-center gap-2 text-white font-bold text-lg">
              <div className="w-8 h-8 rounded-lg bg-brand-600 flex items-center justify-center text-white">
                <Briefcase className="w-4 h-4" />
              </div>
              <span>HireFlow</span>
            </div>
            <p className="text-slate-400 leading-relaxed text-xs">
              Modern end-to-end recruitment platform and Applicant Tracking System (ATS). Empowering teams to discover, evaluate, and hire world-class talent with speed and precision.
            </p>
            <div className="flex items-center gap-3 text-slate-400">
              <a href="#" className="hover:text-white transition-colors"><Globe className="w-4 h-4" /></a>
              <a href="#" className="hover:text-white transition-colors"><Building2 className="w-4 h-4" /></a>
              <a href="#" className="hover:text-white transition-colors"><Sparkles className="w-4 h-4" /></a>
            </div>
          </div>

          {/* Candidates */}
          <div>
            <h4 className="text-white font-semibold mb-3">Job Seekers</h4>
            <ul className="space-y-2">
              <li><Link to="/jobs" className="hover:text-white transition-colors">Browse 100+ Live Jobs</Link></li>
              <li><Link to="/jobs?workplace_type=remote" className="hover:text-white transition-colors">Remote Opportunities</Link></li>
              <li><Link to="/candidate/profile" className="hover:text-white transition-colors">Candidate Profile & CV</Link></li>
              <li><Link to="/candidate/applications" className="hover:text-white transition-colors">Track Applications</Link></li>
            </ul>
          </div>

          {/* Employers */}
          <div>
            <h4 className="text-white font-semibold mb-3">Recruiters & Teams</h4>
            <ul className="space-y-2">
              <li><Link to="/employer/dashboard" className="hover:text-white transition-colors">ATS Workspace</Link></li>
              <li><Link to="/employer/jobs" className="hover:text-white transition-colors">Post Open Positions</Link></li>
              <li><Link to="/employer/ats" className="hover:text-white transition-colors">Kanban Pipeline</Link></li>
              <li><Link to="/pricing" className="hover:text-white transition-colors">SaaS Pricing Plans</Link></li>
            </ul>
          </div>

          {/* System & Trust */}
          <div>
            <h4 className="text-white font-semibold mb-3">System & Trust</h4>
            <div className="space-y-3">
              <div className="flex items-center gap-2 text-emerald-400 font-medium">
                <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                <span>All Systems Operational</span>
              </div>
              <p className="text-[11px] text-slate-500">
                Backed by Django REST Framework 5.0, SQLite with ACID guarantees, JWT secure sessions, and audit trail logging.
              </p>
              <div className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-slate-800 text-slate-300 border border-slate-700">
                <ShieldCheck className="w-3.5 h-3.5 text-brand-400" />
                <span>Enterprise Security Certified</span>
              </div>
            </div>
          </div>
        </div>

        <div className="mt-12 pt-6 border-t border-slate-800 flex flex-col sm:flex-row items-center justify-between gap-4 text-[11px] text-slate-500">
          <p>© {new Date().getFullYear()} HireFlow Inc. All rights reserved.</p>
          <div className="flex items-center gap-4">
            <a href="#" className="hover:text-slate-400">Privacy Policy</a>
            <a href="#" className="hover:text-slate-400">Terms of Service</a>
            <a href="#" className="hover:text-slate-400">Security Audit</a>
            <a href="http://127.0.0.1:8000/api/docs/" target="_blank" rel="noreferrer" className="text-brand-400 hover:text-brand-300 font-medium">Swagger API Docs</a>
          </div>
        </div>
      </div>
    </footer>
  );
};
