from rest_framework import serializers
from apps.jobs.models import JobCategory, Skill, Job, JobSkill, JobReport
from apps.employers.serializers import CompanySerializer

class JobCategorySerializer(serializers.ModelSerializer):
    jobs_count = serializers.SerializerMethodField()

    class Meta:
        model = JobCategory
        fields = ['id', 'name', 'slug', 'icon', 'description', 'is_popular', 'jobs_count']

    def get_jobs_count(self, obj):
        return obj.jobs.filter(status=Job.Status.PUBLISHED).count()


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name', 'slug', 'category', 'is_trending']


class JobSkillSerializer(serializers.ModelSerializer):
    skill_id = serializers.PrimaryKeyRelatedField(queryset=Skill.objects.all(), source='skill')
    skill_name = serializers.ReadOnlyField(source='skill.name')

    class Meta:
        model = JobSkill
        fields = ['id', 'skill_id', 'skill_name', 'is_required']


class JobSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    category_name = serializers.ReadOnlyField(source='category.name')
    skills = JobSkillSerializer(source='job_skills', many=True, read_only=True)
    skills_data = serializers.ListField(
        child=serializers.CharField(), write_only=True, required=False
    )
    is_saved = serializers.SerializerMethodField()
    has_applied = serializers.SerializerMethodField()
    days_remaining = serializers.ReadOnlyField()
    is_expired = serializers.ReadOnlyField()
    total_applicants = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = [
            'id', 'company', 'title', 'slug', 'department', 'category', 'category_name',
            'employment_type', 'workplace_type', 'location', 'min_salary', 'max_salary',
            'salary_currency', 'is_salary_negotiable', 'experience_level', 'education_level',
            'description', 'responsibilities', 'requirements', 'benefits',
            'vacancies', 'deadline', 'status', 'is_featured', 'views_count',
            'skills', 'skills_data', 'is_saved', 'has_applied', 'days_remaining',
            'is_expired', 'total_applicants', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'slug', 'views_count', 'created_at', 'updated_at']

    def get_is_saved(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated and hasattr(request.user, 'candidate_profile'):
            return obj.saved_by_users.filter(candidate=request.user.candidate_profile).exists()
        return False

    def get_has_applied(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated and hasattr(request.user, 'candidate_profile'):
            return obj.applications.filter(candidate=request.user.candidate_profile).exists()
        return False

    def get_total_applicants(self, obj):
        return obj.applications.count()

    def create(self, validated_data):
        skills_data = validated_data.pop('skills_data', [])
        job = Job.objects.create(**validated_data)

        for skill_name in skills_data:
            skill_name_clean = skill_name.strip()
            if skill_name_clean:
                skill, _ = Skill.objects.get_or_create(name=skill_name_clean)
                JobSkill.objects.create(job=job, skill=skill, is_required=True)

        return job

    def update(self, instance, validated_data):
        skills_data = validated_data.pop('skills_data', None)
        job = super().update(instance, validated_data)

        if skills_data is not None:
            job.job_skills.all().delete()
            for skill_name in skills_data:
                skill_name_clean = skill_name.strip()
                if skill_name_clean:
                    skill, _ = Skill.objects.get_or_create(name=skill_name_clean)
                    JobSkill.objects.create(job=job, skill=skill, is_required=True)

        return job


class JobReportSerializer(serializers.ModelSerializer):
    job_title = serializers.ReadOnlyField(source='job.title')
    reporter_email = serializers.ReadOnlyField(source='reporter.email')

    class Meta:
        model = JobReport
        fields = [
            'id', 'job', 'job_title', 'reporter', 'reporter_email',
            'reason', 'details', 'status', 'admin_action_notes',
            'reviewed_by', 'created_at'
        ]
        read_only_fields = ['id', 'reporter', 'status', 'admin_action_notes', 'reviewed_by', 'created_at']
