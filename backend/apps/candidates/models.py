import os
from django.db import models
from django.core.exceptions import ValidationError
from apps.accounts.models import User
from apps.jobs.models import Job, JobCategory, Skill

def validate_resume_file(value):
    ext = os.path.splitext(value.name)[1].lower()
    valid_extensions = ['.pdf', '.doc', '.docx']
    if ext not in valid_extensions:
        raise ValidationError('Only PDF, DOC, and DOCX files are allowed.')
    
    # 10MB limit
    if value.size > 10 * 1024 * 1024:
        raise ValidationError('File size cannot exceed 10MB.')


class CandidateProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='candidate_profile')
    headline = models.CharField(max_length=255, blank=True, default='Full Stack Software Engineer')
    experience_years = models.PositiveIntegerField(default=2)
    preferred_location = models.CharField(max_length=255, blank=True, default='Remote')
    preferred_employment_type = models.CharField(max_length=50, blank=True, default='full_time')
    expected_salary = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    salary_currency = models.CharField(max_length=10, default='USD')
    portfolio_url = models.URLField(max_length=300, blank=True)
    github_url = models.URLField(max_length=300, blank=True)
    linkedin_url = models.URLField(max_length=300, blank=True)
    website_url = models.URLField(max_length=300, blank=True)
    is_open_to_work = models.BooleanField(default=True)
    profile_strength = models.PositiveIntegerField(default=40)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.headline})"

    def calculate_profile_strength(self):
        score = 0
        suggestions = []

        # Check avatar
        if self.user.avatar or self.user.avatar_url:
            score += 10
        else:
            suggestions.append("Upload a profile photo (+10%)")

        # Bio
        if self.user.bio and len(self.user.bio.strip()) > 20:
            score += 15
        else:
            suggestions.append("Add a detailed professional bio (+15%)")

        # Headline
        if self.headline:
            score += 10

        # Skills (at least 3)
        skills_count = self.skills.count()
        if skills_count >= 3:
            score += 20
        elif skills_count > 0:
            score += 10
            suggestions.append("Add at least 3 skills (+10%)")
        else:
            suggestions.append("Add your technical skills (+20%)")

        # Experience
        if self.experiences.exists():
            score += 15
        else:
            suggestions.append("Add your work history (+15%)")

        # Education
        if self.educations.exists():
            score += 10
        else:
            suggestions.append("Add your educational background (+10%)")

        # Resume
        if self.resumes.exists():
            score += 10
        else:
            suggestions.append("Upload your latest CV / Resume (+10%)")

        # Projects / Links
        if self.projects.exists() or self.portfolio_url or self.github_url or self.linkedin_url:
            score += 10
        else:
            suggestions.append("Link your portfolio or GitHub / LinkedIn (+10%)")

        self.profile_strength = min(100, score)
        self.save(update_fields=['profile_strength'])
        return {
            'score': self.profile_strength,
            'suggestions': suggestions
        }


class Education(models.Model):
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='educations')
    institution = models.CharField(max_length=255)
    degree = models.CharField(max_length=150)
    field_of_study = models.CharField(max_length=150)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    grade = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.degree} in {self.field_of_study} at {self.institution}"


class Experience(models.Model):
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='experiences')
    company_name = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255)
    location = models.CharField(max_length=150, blank=True)
    workplace_type = models.CharField(max_length=50, default='hybrid')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    responsibilities = models.JSONField(default=list, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.job_title} at {self.company_name}"


class CandidateSkill(models.Model):
    class ProficiencyLevel(models.TextChoices):
        BEGINNER = 'beginner', 'Beginner'
        INTERMEDIATE = 'intermediate', 'Intermediate'
        ADVANCED = 'advanced', 'Advanced'
        EXPERT = 'expert', 'Expert'

    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='candidates')
    proficiency = models.CharField(max_length=30, choices=ProficiencyLevel.choices, default=ProficiencyLevel.INTERMEDIATE)
    years_of_experience = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('candidate', 'skill')

    def __str__(self):
        return f"{self.skill.name} ({self.proficiency})"


class Project(models.Model):
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=255)
    description = models.TextField()
    technologies = models.JSONField(default=list, blank=True)
    project_url = models.URLField(max_length=300, blank=True)
    repository_url = models.URLField(max_length=300, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return self.title


class Certification(models.Model):
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='certifications')
    name = models.CharField(max_length=255)
    issuing_organization = models.CharField(max_length=255)
    issue_date = models.DateField()
    expiration_date = models.DateField(null=True, blank=True)
    credential_id = models.CharField(max_length=150, blank=True)
    credential_url = models.URLField(max_length=300, blank=True)

    def __str__(self):
        return f"{self.name} - {self.issuing_organization}"


class Resume(models.Model):
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='resumes')
    title = models.CharField(max_length=255, default='My Resume')
    file = models.FileField(upload_to='resumes/', validators=[validate_resume_file], null=True, blank=True)
    file_url = models.URLField(max_length=500, blank=True, null=True)
    is_default = models.BooleanField(default=False)
    file_size_kb = models.PositiveIntegerField(default=0)
    file_extension = models.CharField(max_length=10, default='pdf')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_default', '-uploaded_at']

    def __str__(self):
        return f"{self.title} ({self.candidate.user.get_full_name()})"

    def save(self, *args, **kwargs):
        if self.is_default:
            Resume.objects.filter(candidate=self.candidate).exclude(pk=self.pk).update(is_default=False)
        if self.file and hasattr(self.file, 'size') and not self.file_size_kb:
            self.file_size_kb = max(1, self.file.size // 1024)
            ext = os.path.splitext(self.file.name)[1].lower().replace('.', '')
            self.file_extension = ext
        super().save(*args, **kwargs)


class ResumeBuilder(models.Model):
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='built_resumes')
    title = models.CharField(max_length=200, default='Software Engineer Resume')
    template_name = models.CharField(max_length=50, default='modern')  # modern, executive, minimal, tech
    theme_color = models.CharField(max_length=30, default='#2563eb')
    data = models.JSONField(default=dict)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.candidate.user.get_full_name()})"


class SavedJob(models.Model):
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='saved_jobs')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='saved_by_users')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('candidate', 'job')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.candidate.user.get_full_name()} saved {self.job.title}"


class JobAlert(models.Model):
    class Frequency(models.TextChoices):
        IMMEDIATE = 'immediate', 'Immediate'
        DAILY = 'daily', 'Daily Digest'
        WEEKLY = 'weekly', 'Weekly Digest'

    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='job_alerts')
    title = models.CharField(max_length=200)
    keywords = models.CharField(max_length=255, blank=True)
    category = models.ForeignKey(JobCategory, on_delete=models.SET_NULL, null=True, blank=True)
    location = models.CharField(max_length=255, blank=True)
    employment_type = models.CharField(max_length=50, blank=True)
    frequency = models.CharField(max_length=20, choices=Frequency.choices, default=Frequency.DAILY)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Alert: {self.title} ({self.candidate.user.email})"
