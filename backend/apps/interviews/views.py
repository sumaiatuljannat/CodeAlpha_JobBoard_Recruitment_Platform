from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from apps.interviews.models import Interview
from apps.interviews.serializers import InterviewSerializer
from apps.applications.models import JobApplication, ApplicationStatusHistory
from apps.notifications.models import Notification
from apps.accounts.permissions import IsEmployer, IsAdminUserRole

class InterviewViewSet(viewsets.ModelViewSet):
    serializer_class = InterviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin' or user.is_staff:
            return Interview.objects.all().select_related('application__job', 'application__candidate__user', 'interviewer')
        
        if hasattr(user, 'employer_profile'):
            return Interview.objects.filter(
                application__job__company=user.employer_profile.company
            ).select_related('application__job', 'application__candidate__user', 'interviewer')

        if hasattr(user, 'candidate_profile'):
            return Interview.objects.filter(
                application__candidate=user.candidate_profile
            ).select_related('application__job', 'application__candidate__user', 'interviewer')

        return Interview.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        interview = serializer.save(interviewer=user)
        
        # Move application status to INTERVIEW if not already
        app = interview.application
        if app.status != JobApplication.Status.INTERVIEW:
            old_st = app.status
            app.status = JobApplication.Status.INTERVIEW
            app.save(update_fields=['status'])
            
            ApplicationStatusHistory.objects.create(
                application=app,
                from_status=old_st,
                to_status=JobApplication.Status.INTERVIEW,
                note=f"Interview scheduled for {interview.scheduled_at.strftime('%b %d, %Y at %I:%M %p')}",
                changed_by=user
            )

        # Notify candidate
        time_str = interview.scheduled_at.strftime("%B %d, %Y at %I:%M %p")
        Notification.objects.create(
            recipient=app.candidate.user,
            title=f"Interview Scheduled: {app.job.title}",
            message=f"You have an interview ({interview.get_interview_type_display()}) on {time_str} with {app.job.company.name}.",
            notification_type=Notification.NotificationType.INTERVIEW_INVITE,
            action_url="/candidate/interviews"
        )

    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        interview = self.get_object()
        st = request.data.get('status')
        if not st or st not in Interview.Status.values:
            return Response({'detail': f'Invalid status. Allowed: {Interview.Status.values}'}, status=status.HTTP_400_BAD_REQUEST)
        
        interview.status = st
        if 'feedback' in request.data:
            interview.internal_notes = request.data.get('feedback')
        if 'rating' in request.data:
            interview.rating = request.data.get('rating')
        interview.save()

        return Response({
            'success': True,
            'message': f'Interview status updated to {interview.get_status_display()}',
            'interview': InterviewSerializer(interview).data
        })
