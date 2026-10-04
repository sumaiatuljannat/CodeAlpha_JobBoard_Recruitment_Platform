from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import F, Q, Count
from django.utils import timezone
from apps.jobs.models import JobCategory, Skill, Job, JobSkill, JobReport
from apps.jobs.serializers import (
    JobCategorySerializer,
    SkillSerializer,
    JobSerializer,
    JobReportSerializer
)
from apps.jobs.filters import JobFilter
from apps.accounts.permissions import IsEmployer, IsAdminUserRole

class JobCategoryViewSet(viewsets.ModelViewSet):
    queryset = JobCategory.objects.all().order_by('name')
    serializer_class = JobCategorySerializer
    lookup_field = 'slug'

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'popular']:
            return [permissions.AllowAny()]
        return [IsAdminUserRole()]

    @action(detail=False, methods=['get'])
    def popular(self, request):
        categories = self.queryset.filter(is_popular=True)[:10]
        serializer = self.get_serializer(categories, many=True)
        return Response(serializer.data)


class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all().order_by('name')
    serializer_class = SkillSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'category']

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'trending']:
            return [permissions.AllowAny()]
        return [IsAdminUserRole()]

    @action(detail=False, methods=['get'])
    def trending(self, request):
        trending_skills = self.queryset.filter(is_trending=True)[:15]
        serializer = self.get_serializer(trending_skills, many=True)
        return Response(serializer.data)


class JobViewSet(viewsets.ModelViewSet):
    serializer_class = JobSerializer
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = JobFilter
    search_fields = ['title', 'description', 'company__name', 'location']
    ordering_fields = ['created_at', 'min_salary', 'max_salary', 'views_count']
    ordering = ['-created_at']

    def get_queryset(self):
        user = self.request.user
        qs = Job.objects.select_related('company', 'category', 'posted_by').prefetch_related('job_skills__skill', 'applications')
        
        # Check if caller wants employer's jobs
        is_my_jobs = self.request.query_params.get('my_jobs') == 'true'
        if is_my_jobs and user.is_authenticated and hasattr(user, 'employer_profile'):
            return qs.filter(company=user.employer_profile.company)
            
        # Admin can view all
        if user.is_authenticated and (user.role == 'admin' or user.is_staff):
            return qs
            
        # Public listing: only published & non-expired jobs
        return qs.filter(status=Job.Status.PUBLISHED)

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'featured', 'similar', 'recent']:
            return [permissions.AllowAny()]
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'duplicate', 'pause', 'close', 'reopen']:
            return [IsEmployer()]
        return [permissions.IsAuthenticated()]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Increment views atomically
        Job.objects.filter(pk=instance.pk).update(views_count=F('views_count') + 1)
        instance.refresh_from_db()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def perform_create(self, serializer):
        user = self.request.user
        if not hasattr(user, 'employer_profile'):
            raise permissions.exceptions.PermissionDenied("You must have an employer profile to post jobs.")
        company = user.employer_profile.company
        serializer.save(posted_by=user, company=company)

    @action(detail=False, methods=['get'])
    def featured(self, request):
        featured_jobs = self.get_queryset().filter(is_featured=True)[:6]
        serializer = self.get_serializer(featured_jobs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def recent(self, request):
        recent_jobs = self.get_queryset()[:8]
        serializer = self.get_serializer(recent_jobs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def similar(self, request, slug=None):
        job = self.get_object()
        similar_jobs = Job.objects.filter(
            Q(category=job.category) | Q(employment_type=job.employment_type),
            status=Job.Status.PUBLISHED
        ).exclude(id=job.id).distinct()[:4]
        serializer = self.get_serializer(similar_jobs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsEmployer])
    def duplicate(self, request, slug=None):
        job = self.get_object()
        if job.company != request.user.employer_profile.company:
            return Response({'detail': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
        
        new_job = Job.objects.create(
            company=job.company,
            posted_by=request.user,
            title=f"{job.title} (Copy)",
            department=job.department,
            category=job.category,
            employment_type=job.employment_type,
            workplace_type=job.workplace_type,
            location=job.location,
            min_salary=job.min_salary,
            max_salary=job.max_salary,
            salary_currency=job.salary_currency,
            is_salary_negotiable=job.is_salary_negotiable,
            experience_level=job.experience_level,
            education_level=job.education_level,
            description=job.description,
            responsibilities=job.responsibilities,
            requirements=job.requirements,
            benefits=job.benefits,
            vacancies=job.vacancies,
            deadline=timezone.now() + timezone.timedelta(days=30),
            status=Job.Status.DRAFT,
        )
        for js in job.job_skills.all():
            JobSkill.objects.create(job=new_job, skill=js.skill, is_required=js.is_required)

        serializer = self.get_serializer(new_job)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['patch'], permission_classes=[IsEmployer])
    def pause(self, request, slug=None):
        job = self.get_object()
        job.status = Job.Status.PAUSED
        job.save(update_fields=['status'])
        return Response({'success': True, 'message': 'Job paused.'})

    @action(detail=True, methods=['patch'], permission_classes=[IsEmployer])
    def close(self, request, slug=None):
        job = self.get_object()
        job.status = Job.Status.CLOSED
        job.save(update_fields=['status'])
        return Response({'success': True, 'message': 'Job closed.'})

    @action(detail=True, methods=['patch'], permission_classes=[IsEmployer])
    def reopen(self, request, slug=None):
        job = self.get_object()
        job.status = Job.Status.PUBLISHED
        job.save(update_fields=['status'])
        return Response({'success': True, 'message': 'Job republished.'})


class JobReportViewSet(viewsets.ModelViewSet):
    serializer_class = JobReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin' or user.is_staff:
            return JobReport.objects.all()
        return JobReport.objects.filter(reporter=user)

    def perform_create(self, serializer):
        serializer.save(reporter=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUserRole])
    def resolve(self, request, pk=None):
        report = self.get_object()
        report.status = JobReport.Status.RESOLVED
        report.reviewed_by = request.user
        report.admin_action_notes = request.data.get('notes', 'Action taken by administrator.')
        report.save()

        action_type = request.data.get('action_type')
        if action_type == 'close_job':
            report.job.status = Job.Status.CLOSED
            report.job.save()

        return Response({'success': True, 'message': 'Report resolved.'})
