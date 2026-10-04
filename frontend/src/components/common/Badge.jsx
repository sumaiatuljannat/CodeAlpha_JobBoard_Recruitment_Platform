import React from 'react';

export const StatusBadge = ({ status }) => {
  const map = {
    applied: { label: 'Applied', color: 'bg-blue-50 text-blue-700 border-blue-200' },
    screening: { label: 'Under Review', color: 'bg-purple-50 text-purple-700 border-purple-200' },
    shortlisted: { label: 'Shortlisted', color: 'bg-indigo-50 text-indigo-700 border-indigo-200' },
    interview: { label: 'Interview', color: 'bg-amber-50 text-amber-700 border-amber-200' },
    assessment: { label: 'Assessment', color: 'bg-cyan-50 text-cyan-700 border-cyan-200' },
    offer: { label: 'Offer Made', color: 'bg-emerald-50 text-emerald-700 border-emerald-200' },
    hired: { label: 'Hired 🎉', color: 'bg-green-100 text-green-800 border-green-300 font-semibold' },
    rejected: { label: 'Rejected', color: 'bg-rose-50 text-rose-700 border-rose-200' },
    withdrawn: { label: 'Withdrawn', color: 'bg-slate-100 text-slate-600 border-slate-200' },

    published: { label: 'Published', color: 'bg-emerald-50 text-emerald-700 border-emerald-200' },
    draft: { label: 'Draft', color: 'bg-slate-100 text-slate-600 border-slate-200' },
    paused: { label: 'Paused', color: 'bg-amber-50 text-amber-700 border-amber-200' },
    closed: { label: 'Closed', color: 'bg-rose-50 text-rose-700 border-rose-200' },

    verified: { label: 'Verified', color: 'bg-emerald-50 text-emerald-700 border-emerald-200' },
    pending: { label: 'Pending', color: 'bg-amber-50 text-amber-700 border-amber-200' },
    unverified: { label: 'Unverified', color: 'bg-slate-100 text-slate-500 border-slate-200' },
  };

  const item = map[status?.toLowerCase()] || { label: status, color: 'bg-slate-100 text-slate-600 border-slate-200' };

  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border ${item.color}`}>
      {item.label}
    </span>
  );
};

export const MatchScoreBadge = ({ score }) => {
  let color = 'bg-slate-100 text-slate-700 border-slate-200';
  if (score >= 80) color = 'bg-emerald-50 text-emerald-700 border-emerald-200 font-semibold';
  else if (score >= 65) color = 'bg-blue-50 text-blue-700 border-blue-200 font-medium';
  else if (score >= 50) color = 'bg-amber-50 text-amber-700 border-amber-200';

  return (
    <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs border ${color}`}>
      ⚡ {score}% Match
    </span>
  );
};
