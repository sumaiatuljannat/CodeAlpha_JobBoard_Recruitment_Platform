from rest_framework import viewsets, permissions, status, views, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from apps.candidates.models import (
    CandidateProfile,
    Education,
    Experience,
    CandidateSkill,
    Project,
    Certification,
    Resume,
    ResumeBuilder,
    SavedJob,
    JobAlert
)
from apps.candidates.serializers import (
    CandidateProfileSerializer,
    EducationSerializer,
    ExperienceSerializer,
    CandidateSkillSerializer,
    ProjectSerializer,
    CertificationSerializer,
    ResumeSerializer,
    ResumeBuilderSerializer,
    SavedJobSerializer,
    JobAlertSerializer
)
from apps.jobs.models import Job
from apps.jobs.serializers import JobSerializer
from apps.accounts.permissions import IsCandidate, IsAdminUserRole

class CandidateProfileViewSet(viewsets.ModelViewSet):
    queryset = CandidateProfile.objects.all().select_related('user').prefetch_related(
        'educations', 'experiences', 'skills__skill', 'projects', 'certifications', 'resumes'
    )
    serializer_class = CandidateProfileSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_open_to_work', 'preferred_employment_type']
    search_fields = ['headline', 'user__first_name', 'user__last_name', 'preferred_location', 'skills__skill__name']
    ordering_fields = ['experience_years', 'profile_strength', 'created_at']
    ordering = ['-profile_strength', '-created_at']

    def get_permissions(self):
        if self.action in ['retrieve', 'list']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    @action(detail=False, methods=['get', 'patch'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        profile, _ = CandidateProfile.objects.get_or_create(user=request.user)
        if request.method == 'PATCH':
            serializer = self.get_serializer(profile, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            profile.calculate_profile_strength()
            return Response(serializer.data)
        
        serializer = self.get_serializer(profile)
        return Response(serializer.data)


class EducationViewSet(viewsets.ModelViewSet):
    serializer_class = EducationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if hasattr(self.request.user, 'candidate_profile'):
            return Education.objects.filter(candidate=self.request.user.candidate_profile)
        return Education.objects.none()

    def perform_create(self, serializer):
        profile, _ = CandidateProfile.objects.get_or_create(user=self.request.user)
        serializer.save(candidate=profile)
        profile.calculate_profile_strength()


class ExperienceViewSet(viewsets.ModelViewSet):
    serializer_class = ExperienceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if hasattr(self.request.user, 'candidate_profile'):
            return Experience.objects.filter(candidate=self.request.user.candidate_profile)
        return Experience.objects.none()

    def perform_create(self, serializer):
        profile, _ = CandidateProfile.objects.get_or_create(user=self.request.user)
        serializer.save(candidate=profile)
        profile.calculate_profile_strength()


class CandidateSkillViewSet(viewsets.ModelViewSet):
    serializer_class = CandidateSkillSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if hasattr(self.request.user, 'candidate_profile'):
            return CandidateSkill.objects.filter(candidate=self.request.user.candidate_profile)
        return CandidateSkill.objects.none()

    def perform_create(self, serializer):
        profile, _ = CandidateProfile.objects.get_or_create(user=self.request.user)
        serializer.save(candidate=profile)
        profile.calculate_profile_strength()


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if hasattr(self.request.user, 'candidate_profile'):
            return Project.objects.filter(candidate=self.request.user.candidate_profile)
        return Project.objects.none()

    def perform_create(self, serializer):
        profile, _ = CandidateProfile.objects.get_or_create(user=self.request.user)
        serializer.save(candidate=profile)
        profile.calculate_profile_strength()


class CertificationViewSet(viewsets.ModelViewSet):
    serializer_class = CertificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if hasattr(self.request.user, 'candidate_profile'):
            return Certification.objects.filter(candidate=self.request.user.candidate_profile)
        return Certification.objects.none()

    def perform_create(self, serializer):
        profile, _ = CandidateProfile.objects.get_or_create(user=self.request.user)
        serializer.save(candidate=profile)
        profile.calculate_profile_strength()


class ResumeViewSet(viewsets.ModelViewSet):
    serializer_class = ResumeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if hasattr(self.request.user, 'candidate_profile'):
            return Resume.objects.filter(candidate=self.request.user.candidate_profile)
        return Resume.objects.none()

    def perform_create(self, serializer):
        profile, _ = CandidateProfile.objects.get_or_create(user=self.request.user)
        # If this is the first resume, make it default automatically
        is_first = not profile.resumes.exists()
        serializer.save(candidate=profile, is_default=is_first)
        profile.calculate_profile_strength()

    @action(detail=True, methods=['post'])
    def set_default(self, request, pk=None):
        resume = self.get_object()
        Resume.objects.filter(candidate=resume.candidate).update(is_default=False)
        resume.is_default = True
        resume.save()
        return Response({'success': True, 'message': f'{resume.title} set as default.'})


class ResumeBuilderViewSet(viewsets.ModelViewSet):
    serializer_class = ResumeBuilderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if hasattr(self.request.user, 'candidate_profile'):
            return ResumeBuilder.objects.filter(candidate=self.request.user.candidate_profile)
        return ResumeBuilder.objects.none()

    def perform_create(self, serializer):
        profile, _ = CandidateProfile.objects.get_or_create(user=self.request.user)
        serializer.save(candidate=profile)


class SavedJobViewSet(viewsets.ModelViewSet):
    serializer_class = SavedJobSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if hasattr(self.request.user, 'candidate_profile'):
            return SavedJob.objects.filter(candidate=self.request.user.candidate_profile).select_related('job', 'job__company')
        return SavedJob.objects.none()

    def perform_create(self, serializer):
        profile, _ = CandidateProfile.objects.get_or_create(user=self.request.user)
        serializer.save(candidate=profile)

    @action(detail=False, methods=['post'])
    def toggle(self, request):
        job_id = request.data.get('job_id')
        if not job_id:
            return Response({'detail': 'job_id is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        profile, _ = CandidateProfile.objects.get_or_create(user=request.user)
        saved = SavedJob.objects.filter(candidate=profile, job_id=job_id).first()

        if saved:
            saved.delete()
            return Response({'success': True, 'is_saved': False, 'message': 'Job removed from saved items.'})
        else:
            job = Job.objects.get(pk=job_id)
            SavedJob.objects.create(candidate=profile, job=job)
            return Response({'success': True, 'is_saved': True, 'message': 'Job saved successfully.'})

    @action(detail=False, methods=['post'])
    def compare(self, request):
        job_ids = request.data.get('job_ids', [])
        if not job_ids or len(job_ids) > 4:
            return Response({'detail': 'Please select between 2 and 4 jobs to compare.'}, status=status.HTTP_400_BAD_REQUEST)
        
        jobs = Job.objects.filter(id__in=job_ids)
        serializer = JobSerializer(jobs, many=True, context={'request': request})
        return Response(serializer.data)


class JobAlertViewSet(viewsets.ModelViewSet):
    serializer_class = JobAlertSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if hasattr(self.request.user, 'candidate_profile'):
            return JobAlert.objects.filter(candidate=self.request.user.candidate_profile)
        return JobAlert.objects.none()

    def perform_create(self, serializer):
        profile, _ = CandidateProfile.objects.get_or_create(user=self.request.user)
        serializer.save(candidate=profile)
