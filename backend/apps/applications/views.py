from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from apps.applications.models import JobApplication, ApplicationStatusHistory, RecruiterNote
from apps.applications.serializers import (
    JobApplicationSerializer,
    JobApplicationCreateSerializer,
    ApplicationStatusHistorySerializer,
    RecruiterNoteSerializer
)
from apps.notifications.models import Notification
from apps.accounts.permissions import IsCandidate, IsEmployer, IsAdminUserRole

class JobApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = JobApplicationSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'job_id']
    search_fields = ['candidate__user__first_name', 'candidate__user__last_name', 'candidate__headline', 'job__title']
    ordering_fields = ['created_at', 'match_score', 'updated_at']
    ordering = ['-created_at']

    def get_permissions(self):
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin' or user.is_staff:
            return JobApplication.objects.all().select_related('job', 'job__company', 'candidate__user', 'resume')
        
        if hasattr(user, 'employer_profile'):
            return JobApplication.objects.filter(
                job__company=user.employer_profile.company
            ).select_related('job', 'job__company', 'candidate__user', 'resume').prefetch_related('status_history', 'recruiter_notes')

        if hasattr(user, 'candidate_profile'):
            return JobApplication.objects.filter(
                candidate=user.candidate_profile
            ).select_related('job', 'job__company', 'candidate__user', 'resume').prefetch_related('status_history')

        return JobApplication.objects.none()

    def get_serializer_class(self):
        if self.action == 'create':
            return JobApplicationCreateSerializer
        return JobApplicationSerializer

    def perform_create(self, serializer):
        user = self.request.user
        profile = user.candidate_profile
        application = serializer.save(candidate=profile)
        
        # Calculate AI matching score
        application.calculate_match_score()

        # Log initial status history
        ApplicationStatusHistory.objects.create(
            application=application,
            from_status='',
            to_status=JobApplication.Status.APPLIED,
            note='Application successfully submitted by candidate.',
            changed_by=user
        )

        # Notify Employer
        job_poster = application.job.posted_by
        Notification.objects.create(
            recipient=job_poster,
            title=f"New applicant for {application.job.title}",
            message=f"{user.get_full_name()} just applied for '{application.job.title}' with a {application.match_score}% match score.",
            notification_type=Notification.NotificationType.NEW_APPLICATION,
            action_url=f"/employer/ats?job={application.job.id}"
        )

        # Notify Candidate
        Notification.objects.create(
            recipient=user,
            title=f"Application sent: {application.job.title}",
            message=f"Your application for '{application.job.title}' at {application.job.company.name} has been received.",
            notification_type=Notification.NotificationType.APPLICATION_STATUS,
            action_url=f"/candidate/applications"
        )

    @action(detail=True, methods=['patch'], permission_classes=[IsEmployer])
    def change_status(self, request, pk=None):
        application = self.get_object()
        new_status = request.data.get('status')
        note = request.data.get('note', '')

        if not new_status or new_status not in JobApplication.Status.values:
            return Response({'detail': f'Invalid status. Allowed: {JobApplication.Status.values}'}, status=status.HTTP_400_BAD_REQUEST)

        old_status = application.status
        application.status = new_status
        if new_status == JobApplication.Status.REJECTED:
            application.rejection_reason = note
        application.save()

        # Record history
        ApplicationStatusHistory.objects.create(
            application=application,
            from_status=old_status,
            to_status=new_status,
            note=note or f"Status changed to {application.get_status_display()}",
            changed_by=request.user
        )

        # Notify Candidate
        status_readable = application.get_status_display()
        Notification.objects.create(
            recipient=application.candidate.user,
            title=f"Update on your application for {application.job.title}",
            message=f"Your application status has been updated to '{status_readable}' by {application.job.company.name}.",
            notification_type=Notification.NotificationType.APPLICATION_STATUS,
            action_url="/candidate/applications"
        )

        return Response({
            'success': True,
            'message': f'Status updated to {status_readable}.',
            'application': JobApplicationSerializer(application).data
        })

    @action(detail=True, methods=['post'], permission_classes=[IsCandidate])
    def withdraw(self, request, pk=None):
        application = self.get_object()
        if application.candidate.user != request.user:
            return Response({'detail': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
        
        reason = request.data.get('reason', 'Withdrawn by candidate.')
        old_status = application.status
        application.status = JobApplication.Status.WITHDRAWN
        application.withdrawal_reason = reason
        application.save()

        ApplicationStatusHistory.objects.create(
            application=application,
            from_status=old_status,
            to_status=JobApplication.Status.WITHDRAWN,
            note=reason,
            changed_by=request.user
        )

        # Notify Employer
        Notification.objects.create(
            recipient=application.job.posted_by,
            title=f"Application withdrawn: {application.job.title}",
            message=f"{request.user.get_full_name()} has withdrawn their application for '{application.job.title}'.",
            notification_type=Notification.NotificationType.SYSTEM,
            action_url=f"/employer/ats?job={application.job.id}"
        )

        return Response({'success': True, 'message': 'Application withdrawn successfully.'})

    @action(detail=True, methods=['post'], permission_classes=[IsEmployer])
    def add_note(self, request, pk=None):
        application = self.get_object()
        note_text = request.data.get('note', '').strip()
        is_private = request.data.get('is_private', True)
        
        if not note_text:
            return Response({'detail': 'Note content is required.'}, status=status.HTTP_400_BAD_REQUEST)

        note = RecruiterNote.objects.create(
            application=application,
            author=request.user,
            note=note_text,
            is_private=is_private
        )
        return Response(RecruiterNoteSerializer(note).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'], permission_classes=[IsEmployer])
    def kanban(self, request):
        job_id = request.query_params.get('job_id')
        user = request.user
        
        qs = JobApplication.objects.filter(job__company=user.employer_profile.company).select_related(
            'job', 'candidate__user', 'resume'
        )
        if job_id:
            qs = qs.filter(job_id=job_id)

        columns = {
            'applied': [],
            'screening': [],
            'shortlisted': [],
            'interview': [],
            'assessment': [],
            'offer': [],
            'hired': [],
            'rejected': [],
        }

        for app in qs:
            st = app.status
            if st in columns:
                columns[st].append(JobApplicationSerializer(app).data)

        return Response({
            'success': True,
            'columns': columns,
            'total_count': qs.count()
        })
