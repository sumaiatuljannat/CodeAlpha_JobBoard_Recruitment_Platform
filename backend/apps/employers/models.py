from django.db import models
from django.utils.text import slugify
from apps.accounts.models import User

class Company(models.Model):
    class CompanySize(models.TextChoices):
        SIZE_1_10 = '1-10', '1-10 Employees'
        SIZE_11_50 = '11-50', '11-50 Employees'
        SIZE_51_200 = '51-200', '51-200 Employees'
        SIZE_201_500 = '201-500', '201-500 Employees'
        SIZE_501_1000 = '501-1000', '501-1000 Employees'
        SIZE_1000_PLUS = '1000+', '1000+ Employees'

    class VerificationStatus(models.TextChoices):
        UNVERIFIED = 'unverified', 'Unverified'
        PENDING = 'pending', 'Pending Verification'
        VERIFIED = 'verified', 'Verified'
        REJECTED = 'rejected', 'Rejected'

    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=280, unique=True, blank=True)
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    logo_url = models.URLField(max_length=500, blank=True, null=True)
    cover_image = models.ImageField(upload_to='company_covers/', blank=True, null=True)
    cover_image_url = models.URLField(max_length=500, blank=True, null=True)
    industry = models.CharField(max_length=150, db_index=True)
    company_size = models.CharField(max_length=30, choices=CompanySize.choices, default=CompanySize.SIZE_11_50)
    founded_year = models.PositiveIntegerField(null=True, blank=True)
    headquarters = models.CharField(max_length=255)
    website = models.URLField(max_length=300, blank=True)
    about = models.TextField()
    mission = models.TextField(blank=True, default='')
    benefits = models.JSONField(default=list, blank=True)  # ['Health Insurance', 'Remote Flexibility', '401k']
    social_links = models.JSONField(default=dict, blank=True)  # {'linkedin': '', 'twitter': '', 'github': ''}
    is_verified = models.BooleanField(default=False, db_index=True)
    verification_status = models.CharField(
        max_length=20,
        choices=VerificationStatus.choices,
        default=VerificationStatus.UNVERIFIED,
        db_index=True
    )
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Companies'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Company.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    @property
    def display_logo(self):
        if self.logo:
            return self.logo.url
        if self.logo_url:
            return self.logo_url
        return f"https://api.dicebear.com/7.x/identicon/svg?seed={self.slug}"

    @property
    def display_cover(self):
        if self.cover_image:
            return self.cover_image.url
        if self.cover_image_url:
            return self.cover_image_url
        return "https://images.unsplash.com/photo-1497215728101-856f4ea42174?w=1200&auto=format&fit=crop&q=80"


class EmployerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employer_profile')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='recruiters')
    designation = models.CharField(max_length=150, blank=True, default='Talent Acquisition Lead')
    department = models.CharField(max_length=100, blank=True, default='Human Resources')
    role_in_company = models.CharField(max_length=50, default='admin')
    is_primary = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name()} @ {self.company.name}"


class CompanyVerification(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='verification_requests')
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submitted_verifications')
    trade_license_number = models.CharField(max_length=100, blank=True)
    tax_id = models.CharField(max_length=100, blank=True)
    official_document = models.FileField(upload_to='verification_docs/', blank=True, null=True)
    official_document_url = models.URLField(max_length=500, blank=True, null=True)
    notes = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=Company.VerificationStatus.choices,
        default=Company.VerificationStatus.PENDING
    )
    admin_notes = models.TextField(blank=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_verifications')
    reviewed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Verification for {self.company.name} ({self.status})"


class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    price_monthly = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    price_yearly = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    job_post_limit = models.IntegerField(default=5)
    candidate_views_limit = models.IntegerField(default=100)
    team_members_limit = models.IntegerField(default=3)
    features = models.JSONField(default=list, blank=True)
    is_popular = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} (${self.price_monthly}/mo)"


class CompanySubscription(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        TRIALING = 'trialing', 'Trialing'
        PAST_DUE = 'past_due', 'Past Due'
        CANCELED = 'canceled', 'Canceled'

    company = models.OneToOneField(Company, on_delete=models.CASCADE, related_name='subscription')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True, related_name='subscriptions')
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.ACTIVE)
    billing_interval = models.CharField(max_length=20, default='monthly')
    current_period_start = models.DateTimeField(auto_now_add=True)
    current_period_end = models.DateTimeField(null=True, blank=True)
    payment_method = models.CharField(max_length=100, default='Commercial B2B Invoicing (Net 30)')
    auto_renew = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.company.name} - {self.plan.name if self.plan else 'Custom'} ({self.status})"

