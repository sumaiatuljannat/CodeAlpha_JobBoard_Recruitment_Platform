from rest_framework import serializers
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
from apps.accounts.serializers import UserSerializer
from apps.jobs.serializers import JobSerializer, SkillSerializer
from apps.jobs.models import Skill, Job

class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'
        read_only_fields = ['id', 'candidate']


class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = '__all__'
        read_only_fields = ['id', 'candidate']


class CandidateSkillSerializer(serializers.ModelSerializer):
    skill_id = serializers.PrimaryKeyRelatedField(queryset=Skill.objects.all(), source='skill')
    skill_name = serializers.ReadOnlyField(source='skill.name')

    class Meta:
        model = CandidateSkill
        fields = ['id', 'skill_id', 'skill_name', 'proficiency', 'years_of_experience']
        read_only_fields = ['id']


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ['id', 'candidate']


class CertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certification
        fields = '__all__'
        read_only_fields = ['id', 'candidate']


class ResumeSerializer(serializers.ModelSerializer):
    file_url_display = serializers.SerializerMethodField()

    class Meta:
        model = Resume
        fields = ['id', 'title', 'file', 'file_url', 'file_url_display', 'is_default', 'file_size_kb', 'file_extension', 'uploaded_at']
        read_only_fields = ['id', 'file_size_kb', 'file_extension', 'uploaded_at']

    def get_file_url_display(self, obj):
        if obj.file:
            return obj.file.url
        return obj.file_url or ''


class ResumeBuilderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumeBuilder
        fields = ['id', 'title', 'template_name', 'theme_color', 'data', 'updated_at']
        read_only_fields = ['id', 'updated_at']


class SavedJobSerializer(serializers.ModelSerializer):
    job_details = JobSerializer(source='job', read_only=True)
    job_id = serializers.PrimaryKeyRelatedField(queryset=Job.objects.all(), source='job', write_only=True)

    class Meta:
        model = SavedJob
        fields = ['id', 'job_id', 'job_details', 'created_at']
        read_only_fields = ['id', 'created_at']


class JobAlertSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = JobAlert
        fields = ['id', 'title', 'keywords', 'category', 'category_name', 'location', 'employment_type', 'frequency', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']


class CandidateProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    educations = EducationSerializer(many=True, read_only=True)
    experiences = ExperienceSerializer(many=True, read_only=True)
    skills = CandidateSkillSerializer(many=True, read_only=True)
    projects = ProjectSerializer(many=True, read_only=True)
    certifications = CertificationSerializer(many=True, read_only=True)
    resumes = ResumeSerializer(many=True, read_only=True)
    profile_strength_details = serializers.SerializerMethodField()

    class Meta:
        model = CandidateProfile
        fields = [
            'id', 'user', 'headline', 'experience_years', 'preferred_location',
            'preferred_employment_type', 'expected_salary', 'salary_currency',
            'portfolio_url', 'github_url', 'linkedin_url', 'website_url',
            'is_open_to_work', 'profile_strength', 'profile_strength_details',
            'educations', 'experiences', 'skills', 'projects', 'certifications', 'resumes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'profile_strength', 'created_at', 'updated_at']

    def get_profile_strength_details(self, obj):
        return obj.calculate_profile_strength()
