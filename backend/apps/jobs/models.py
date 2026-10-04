from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from apps.accounts.models import User
from apps.employers.models import Company

class JobCategory(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    icon = models.CharField(max_length=60, default='Briefcase')
    description = models.TextField(blank=True)
    is_popular = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Job Categories'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    category = models.CharField(max_length=100, blank=True, default='General')
    is_trending = models.BooleanField(default=False)

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Job(models.Model):
    class EmploymentType(models.TextChoices):
        FULL_TIME = 'full_time', 'Full-time'
        PART_TIME = 'part_time', 'Part-time'
        CONTRACT = 'contract', 'Contract'
        INTERNSHIP = 'internship', 'Internship'
        FREELANCE = 'freelance', 'Freelance'
        REMOTE = 'remote', 'Remote'

    class WorkplaceType(models.TextChoices):
        ON_SITE = 'on_site', 'On-site'
        HYBRID = 'hybrid', 'Hybrid'
        REMOTE = 'remote', 'Remote'

    class ExperienceLevel(models.TextChoices):
        ENTRY = 'entry', 'Entry Level (0-1 yrs)'
        JUNIOR = 'junior', 'Junior (1-3 yrs)'
        MID = 'mid', 'Mid Level (3-5 yrs)'
        SENIOR = 'senior', 'Senior (5-8 yrs)'
        LEAD = 'lead', 'Lead / Principal (8+ yrs)'
        EXECUTIVE = 'executive', 'Executive / VP'

    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        PUBLISHED = 'published', 'Published'
        PAUSED = 'paused', 'Paused'
        CLOSED = 'closed', 'Closed'
        EXPIRED = 'expired', 'Expired'

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='jobs')
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posted_jobs')
    title = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=280, unique=True, blank=True)
    department = models.CharField(max_length=120, blank=True, default='Engineering')
    category = models.ForeignKey(JobCategory, on_delete=models.SET_NULL, null=True, related_name='jobs')
    employment_type = models.CharField(max_length=30, choices=EmploymentType.choices, default=EmploymentType.FULL_TIME, db_index=True)
    workplace_type = models.CharField(max_length=30, choices=WorkplaceType.choices, default=WorkplaceType.HYBRID, db_index=True)
    location = models.CharField(max_length=255, db_index=True)
    min_salary = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    max_salary = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    salary_currency = models.CharField(max_length=10, default='USD')
    is_salary_negotiable = models.BooleanField(default=False)
    experience_level = models.CharField(max_length=30, choices=ExperienceLevel.choices, default=ExperienceLevel.MID, db_index=True)
    education_level = models.CharField(max_length=150, blank=True, default="Bachelor's Degree in Computer Science or related field")
    
    description = models.TextField()
    responsibilities = models.JSONField(default=list, blank=True)  # List of bullet points
    requirements = models.JSONField(default=list, blank=True)      # List of bullet points
    benefits = models.JSONField(default=list, blank=True)          # List of perks
    
    vacancies = models.PositiveIntegerField(default=1)
    deadline = models.DateTimeField(null=True, blank=True, db_index=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PUBLISHED, db_index=True)
    is_featured = models.BooleanField(default=False, db_index=True)
    views_count = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.company.name}-{self.title}")
            slug = base_slug
            counter = 1
            while Job.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} at {self.company.name}"

    @property
    def is_expired(self):
        if self.deadline and timezone.now() > self.deadline:
            return True
        return self.status == self.Status.EXPIRED

    @property
    def days_remaining(self):
        if not self.deadline:
            return None
        diff = self.deadline - timezone.now()
        return max(0, diff.days)


class JobSkill(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='job_skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='skill_jobs')
    is_required = models.BooleanField(default=True)  # True = Required, False = Preferred

    class Meta:
        unique_together = ('job', 'skill')

    def __str__(self):
        return f"{self.skill.name} ({'Required' if self.is_required else 'Preferred'}) for {self.job.title}"


class JobReport(models.Model):
    class Reason(models.TextChoices):
        SCAM = 'scam', 'Fraud or Scam'
        FAKE_COMPANY = 'fake_company', 'Fake Company or Impersonation'
        MISLEADING_SALARY = 'misleading_salary', 'Misleading Salary / Job Details'
        INAPPROPRIATE = 'inappropriate', 'Inappropriate or Discriminatory Content'
        DUPLICATE = 'duplicate', 'Duplicate Listing'
        OTHER = 'other', 'Other Violation'

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending Review'
        RESOLVED = 'resolved', 'Resolved / Action Taken'
        DISMISSED = 'dismissed', 'Dismissed'

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='reports')
    reporter = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reported_jobs')
    reason = models.CharField(max_length=40, choices=Reason.choices)
    details = models.TextField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING, db_index=True)
    admin_action_notes = models.TextField(blank=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='moderated_reports')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Report #{self.id} on {self.job.title} ({self.reason})"
