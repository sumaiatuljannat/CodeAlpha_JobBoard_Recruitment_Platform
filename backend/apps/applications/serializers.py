from rest_framework import serializers
from apps.applications.models import JobApplication, ApplicationStatusHistory, RecruiterNote
from apps.jobs.serializers import JobSerializer
from apps.candidates.serializers import CandidateProfileSerializer, ResumeSerializer
from apps.accounts.serializers import UserSerializer

class ApplicationStatusHistorySerializer(serializers.ModelSerializer):
    changed_by_name = serializers.ReadOnlyField(source='changed_by.get_full_name')

    class Meta:
        model = ApplicationStatusHistory
        fields = ['id', 'from_status', 'to_status', 'note', 'changed_by', 'changed_by_name', 'created_at']


class RecruiterNoteSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source='author.get_full_name')
    author_avatar = serializers.ReadOnlyField(source='author.display_avatar')

    class Meta:
        model = RecruiterNote
        fields = ['id', 'author', 'author_name', 'author_avatar', 'note', 'is_private', 'created_at']
        read_only_fields = ['id', 'author', 'created_at']


class JobApplicationSerializer(serializers.ModelSerializer):
    job = JobSerializer(read_only=True)
    candidate = CandidateProfileSerializer(read_only=True)
    resume = ResumeSerializer(read_only=True)
    status_history = ApplicationStatusHistorySerializer(many=True, read_only=True)
    recruiter_notes = RecruiterNoteSerializer(many=True, read_only=True)

    class Meta:
        model = JobApplication
        fields = [
            'id', 'job', 'candidate', 'resume', 'cover_letter', 'expected_salary',
            'availability_notice', 'status', 'match_score', 'match_reasons',
            'rejection_reason', 'withdrawal_reason', 'status_history', 'recruiter_notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'match_score', 'match_reasons', 'created_at', 'updated_at']


class JobApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = ['job', 'resume', 'cover_letter', 'expected_salary', 'availability_notice']

    def validate(self, attrs):
        request = self.context.get('request')
        user = request.user
        job = attrs.get('job')
        
        if not hasattr(user, 'candidate_profile'):
            raise serializers.ValidationError('You must create a candidate profile to apply for jobs.')
        
        if JobApplication.objects.filter(job=job, candidate=user.candidate_profile).exists():
            raise serializers.ValidationError('You have already applied for this position.')

        if job.is_expired or job.status != 'published':
            raise serializers.ValidationError('This job is no longer accepting applications.')

        return attrs
