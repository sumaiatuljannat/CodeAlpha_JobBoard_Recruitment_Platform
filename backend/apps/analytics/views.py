import csv
from datetime import timedelta
from django.http import HttpResponse
from django.utils import timezone
from django.db.models import Count, Q
from rest_framework import views, permissions, status
from rest_framework.response import Response

from apps.accounts.models import User
from apps.employers.models import Company, CompanyVerification
from apps.jobs.models import Job, JobCategory, JobReport
from apps.candidates.models import CandidateProfile, SavedJob
from apps.applications.models import JobApplication
from apps.interviews.models import Interview
from apps.jobs.serializers import JobSerializer
from apps.accounts.permissions import IsEmployer, IsCandidate, IsAdminUserRole

class EmployerAnalyticsView(views.APIView):
    permission_classes = [IsEmployer]

    def get(self, request):
        user = request.user
        if not hasattr(user, 'employer_profile'):
            return Response({'detail': 'Employer profile required.'}, status=status.HTTP_404_NOT_FOUND)

        company = user.employer_profile.company
        jobs = Job.objects.filter(company=company)
        job_ids = list(jobs.values_list('id', flat=True))

        total_jobs = jobs.count()
        active_jobs = jobs.filter(status=Job.Status.PUBLISHED).count()

        applications = JobApplication.objects.filter(job_id__in=job_ids)
        total_applications = applications.count()
        
        shortlisted_count = applications.filter(status=JobApplication.Status.SHORTLISTED).count()
        interview_count = applications.filter(status=JobApplication.Status.INTERVIEW).count()
        offer_count = applications.filter(status=JobApplication.Status.OFFER).count()
        hired_count = applications.filter(status=JobApplication.Status.HIRED).count()
        rejected_count = applications.filter(status=JobApplication.Status.REJECTED).count()

        # Rates
        shortlist_rate = round((shortlisted_count / max(1, total_applications)) * 100, 1)
        interview_rate = round((interview_count / max(1, total_applications)) * 100, 1)
        hire_rate = round((hired_count / max(1, total_applications)) * 100, 1)

        # 14-day Application trend
        now = timezone.now()
        trend = []
        for i in range(13, -1, -1):
            day_start = now - timedelta(days=i)
            day_label = day_start.strftime("%b %d")
            day_count = applications.filter(
                created_at__date=day_start.date()
            ).count()
            trend.append({'date': day_label, 'applications': day_count})

        # Top jobs by applicants
        top_jobs = []
        for j in jobs.annotate(app_count=Count('applications')).order_by('-app_count')[:5]:
            top_jobs.append({
                'id': j.id,
                'title': j.title,
                'status': j.status,
                'views': j.views_count,
                'applications': j.app_count,
                'created_at': j.created_at.strftime('%Y-%m-%d')
            })

        # Candidate Experience Distribution
        exp_dist = [
            {'name': 'Entry (0-1y)', 'value': applications.filter(candidate__experience_years__lte=1).count()},
            {'name': 'Junior (2-3y)', 'value': applications.filter(candidate__experience_years__in=[2, 3]).count()},
            {'name': 'Mid (4-6y)', 'value': applications.filter(candidate__experience_years__in=[4, 5, 6]).count()},
            {'name': 'Senior (7y+)', 'value': applications.filter(candidate__experience_years__gte=7).count()},
        ]

        return Response({
            'success': True,
            'summary': {
                'total_jobs': total_jobs,
                'active_jobs': active_jobs,
                'total_applications': total_applications,
                'shortlisted_count': shortlisted_count,
                'interview_count': interview_count,
                'offer_count': offer_count,
                'hired_count': hired_count,
                'rejected_count': rejected_count,
                'shortlist_rate': shortlist_rate,
                'interview_rate': interview_rate,
                'hire_rate': hire_rate,
                'avg_time_to_hire_days': 18,
            },
            'pipeline_funnel': [
                {'stage': 'Applied', 'count': total_applications, 'fill': '#3b82f6'},
                {'stage': 'Reviewing', 'count': applications.filter(status=JobApplication.Status.SCREENING).count(), 'fill': '#6366f1'},
                {'stage': 'Shortlisted', 'count': shortlisted_count, 'fill': '#8b5cf6'},
                {'stage': 'Interview', 'count': interview_count, 'fill': '#ec4899'},
                {'stage': 'Offer', 'count': offer_count, 'fill': '#f59e0b'},
                {'stage': 'Hired', 'count': hired_count, 'fill': '#10b981'},
            ],
            'application_trend': trend,
            'top_jobs': top_jobs,
            'candidate_experience_distribution': exp_dist,
        })


class CandidateDashboardView(views.APIView):
    permission_classes = [IsCandidate]

    def get(self, request):
        user = request.user
        profile, _ = CandidateProfile.objects.get_or_create(user=user)
        strength_info = profile.calculate_profile_strength()

        # Applications count by status
        apps = JobApplication.objects.filter(candidate=profile)
        total_apps = apps.count()
        applied_count = apps.filter(status=JobApplication.Status.APPLIED).count()
        review_count = apps.filter(status=JobApplication.Status.SCREENING).count()
        shortlisted_count = apps.filter(status=JobApplication.Status.SHORTLISTED).count()
        interview_count = apps.filter(status=JobApplication.Status.INTERVIEW).count()
        offer_count = apps.filter(status=JobApplication.Status.OFFER).count()
        hired_count = apps.filter(status=JobApplication.Status.HIRED).count()
        rejected_count = apps.filter(status=JobApplication.Status.REJECTED).count()

        # Upcoming interviews
        upcoming_interviews = []
        for interview in Interview.objects.filter(
            application__candidate=profile,
            status=Interview.Status.SCHEDULED,
            scheduled_at__gte=timezone.now()
        ).order_by('scheduled_at')[:4]:
            upcoming_interviews.append({
                'id': interview.id,
                'title': interview.title,
                'type': interview.get_interview_type_display(),
                'company': interview.application.job.company.name,
                'job_title': interview.application.job.title,
                'scheduled_at': interview.scheduled_at,
                'meeting_link': interview.meeting_link,
            })

        # Saved jobs count
        saved_count = SavedJob.objects.filter(candidate=profile).count()

        # Smart Recommendation Algorithm
        user_skills = set(profile.skills.values_list('skill__name', flat=True))
        all_published_jobs = Job.objects.filter(status=Job.Status.PUBLISHED).select_related('company', 'category').prefetch_related('job_skills__skill')

        recommendations = []
        applied_job_ids = set(apps.values_list('job_id', flat=True))

        for job in all_published_jobs:
            if job.id in applied_job_ids:
                continue

            match_score = 40
            match_points = []
            
            # Check skill overlap
            job_skill_names = set(job.job_skills.values_list('skill__name', flat=True))
            overlap = user_skills.intersection(job_skill_names)
            if overlap:
                match_score += min(35, len(overlap) * 12)
                match_points.append(f"{len(overlap)} matching skills ({', '.join(list(overlap)[:3])})")

            # Check location/remote preference
            if job.workplace_type == Job.WorkplaceType.REMOTE or (profile.preferred_location and profile.preferred_location.lower() in job.location.lower()):
                match_score += 15
                match_points.append("Location preference aligned")

            # Experience alignment
            if profile.experience_years >= 2:
                match_score += 10
                match_points.append("Experience criteria met")

            if not match_points:
                match_points.append("Relevant opportunity in your industry")

            final_score = min(96, match_score)
            if final_score >= 50 or len(recommendations) < 6:
                job_data = JobSerializer(job, context={'request': request}).data
                job_data['recommendation_score'] = final_score
                job_data['recommendation_reasons'] = match_points
                recommendations.append(job_data)

        # Sort recommendations by highest score
        recommendations = sorted(recommendations, key=lambda x: x['recommendation_score'], reverse=True)[:8]

        return Response({
            'success': True,
            'profile_strength': strength_info['score'],
            'suggestions': strength_info['suggestions'],
            'application_stats': {
                'total': total_apps,
                'applied': applied_count,
                'reviewing': review_count,
                'shortlisted': shortlisted_count,
                'interview': interview_count,
                'offer': offer_count,
                'hired': hired_count,
                'rejected': rejected_count,
            },
            'saved_jobs_count': saved_count,
            'upcoming_interviews': upcoming_interviews,
            'recommendations': recommendations,
        })


class AdminAnalyticsView(views.APIView):
    permission_classes = [IsAdminUserRole]

    def get(self, request):
        total_users = User.objects.count()
        candidates_count = User.objects.filter(role=User.Role.CANDIDATE).count()
        employers_count = User.objects.filter(role=User.Role.EMPLOYER).count()
        companies_count = Company.objects.count()
        verified_companies_count = Company.objects.filter(is_verified=True).count()
        pending_verifications = CompanyVerification.objects.filter(status='pending').count()
        
        total_jobs = Job.objects.count()
        active_jobs = Job.objects.filter(status=Job.Status.PUBLISHED).count()
        total_applications = JobApplication.objects.count()
        total_hires = JobApplication.objects.filter(status=JobApplication.Status.HIRED).count()
        reported_jobs_count = JobReport.objects.filter(status=JobReport.Status.PENDING).count()
        suspended_users_count = User.objects.filter(is_active=False).count()

        # Job distribution by category
        categories_data = []
        for cat in JobCategory.objects.annotate(cat_jobs=Count('jobs')).order_by('-cat_jobs')[:8]:
            categories_data.append({
                'name': cat.name,
                'jobs': cat.cat_jobs
            })

        # 30-day Growth Trend
        now = timezone.now()
        trend = []
        for i in range(29, -1, -3):
            d = now - timedelta(days=i)
            d_label = d.strftime("%b %d")
            users_up_to = User.objects.filter(created_at__lte=d).count()
            jobs_up_to = Job.objects.filter(created_at__lte=d).count()
            apps_up_to = JobApplication.objects.filter(created_at__lte=d).count()
            trend.append({
                'date': d_label,
                'users': users_up_to,
                'jobs': jobs_up_to,
                'applications': apps_up_to
            })

        return Response({
            'success': True,
            'stats': {
                'total_users': total_users,
                'candidates_count': candidates_count,
                'employers_count': employers_count,
                'companies_count': companies_count,
                'verified_companies_count': verified_companies_count,
                'pending_verifications': pending_verifications,
                'total_jobs': total_jobs,
                'active_jobs': active_jobs,
                'total_applications': total_applications,
                'total_hires': total_hires,
                'reported_jobs_count': reported_jobs_count,
                'suspended_users_count': suspended_users_count,
            },
            'categories_distribution': categories_data,
            'growth_trend': trend,
        })


class AdminExportCSVView(views.APIView):
    permission_classes = [IsAdminUserRole]

    def get(self, request):
        resource = request.query_params.get('type', 'jobs')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="hiresphere_{resource}_report.csv"'
        writer = csv.writer(response)

        if resource == 'jobs':
            writer.writerow(['ID', 'Title', 'Company', 'Category', 'Employment Type', 'Workplace Type', 'Location', 'Min Salary', 'Max Salary', 'Status', 'Views', 'Created At'])
            for j in Job.objects.select_related('company', 'category').all():
                writer.writerow([j.id, j.title, j.company.name, j.category.name if j.category else '', j.employment_type, j.workplace_type, j.location, j.min_salary or 0, j.max_salary or 0, j.status, j.views_count, j.created_at])

        elif resource == 'users':
            writer.writerow(['ID', 'Email', 'Full Name', 'Role', 'Is Active', 'Is Verified', 'Date Joined'])
            for u in User.objects.all():
                writer.writerow([u.id, u.email, u.get_full_name(), u.role, u.is_active, u.is_email_verified, u.created_at])

        elif resource == 'applications':
            writer.writerow(['ID', 'Job Title', 'Company', 'Candidate Name', 'Candidate Email', 'Status', 'Match Score', 'Applied At'])
            for a in JobApplication.objects.select_related('job__company', 'candidate__user').all():
                writer.writerow([a.id, a.job.title, a.job.company.name, a.candidate.user.get_full_name(), a.candidate.user.email, a.status, a.match_score, a.created_at])

        return response
