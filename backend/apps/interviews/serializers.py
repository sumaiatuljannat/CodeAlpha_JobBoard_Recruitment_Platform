from rest_framework import serializers
from apps.interviews.models import Interview
from apps.applications.serializers import JobApplicationSerializer
from apps.accounts.serializers import UserSerializer

class InterviewSerializer(serializers.ModelSerializer):
    application_details = JobApplicationSerializer(source='application', read_only=True)
    interviewer_details = UserSerializer(source='interviewer', read_only=True)
    candidate_name = serializers.ReadOnlyField(source='application.candidate.user.get_full_name')
    candidate_email = serializers.ReadOnlyField(source='application.candidate.user.email')
    job_title = serializers.ReadOnlyField(source='application.job.title')
    company_name = serializers.ReadOnlyField(source='application.job.company.name')

    class Meta:
        model = Interview
        fields = [
            'id', 'application', 'application_details', 'interviewer', 'interviewer_details',
            'candidate_name', 'candidate_email', 'job_title', 'company_name',
            'title', 'interview_type', 'scheduled_at', 'duration_minutes', 'meeting_link',
            'location', 'instructions', 'status', 'candidate_feedback', 'internal_notes',
            'rating', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'interviewer', 'created_at', 'updated_at']
