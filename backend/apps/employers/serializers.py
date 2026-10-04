from rest_framework import serializers
from apps.employers.models import Company, EmployerProfile, CompanyVerification, SubscriptionPlan, CompanySubscription
from apps.accounts.serializers import UserSerializer

class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = '__all__'


class CompanySubscriptionSerializer(serializers.ModelSerializer):
    plan = SubscriptionPlanSerializer(read_only=True)
    plan_id = serializers.PrimaryKeyRelatedField(
        queryset=SubscriptionPlan.objects.all(), source='plan', write_only=True, required=False
    )

    class Meta:
        model = CompanySubscription
        fields = [
            'id', 'company', 'plan', 'plan_id', 'status', 'billing_interval',
            'current_period_start', 'current_period_end', 'payment_method', 'auto_renew', 'updated_at'
        ]


class CompanySerializer(serializers.ModelSerializer):
    display_logo = serializers.ReadOnlyField()
    display_cover = serializers.ReadOnlyField()
    active_jobs_count = serializers.SerializerMethodField()
    subscription = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = [
            'id', 'name', 'slug', 'logo', 'logo_url', 'display_logo',
            'cover_image', 'cover_image_url', 'display_cover',
            'industry', 'company_size', 'founded_year', 'headquarters',
            'website', 'about', 'mission', 'benefits', 'social_links',
            'is_verified', 'verification_status', 'is_featured',
            'active_jobs_count', 'subscription', 'created_at'
        ]
        read_only_fields = ['id', 'slug', 'is_verified', 'verification_status', 'created_at']

    def get_active_jobs_count(self, obj):
        return obj.jobs.filter(status='published').count()

    def get_subscription(self, obj):
        if hasattr(obj, 'subscription'):
            return {
                'plan_name': obj.subscription.plan.name if obj.subscription.plan else 'Starter Free',
                'plan_slug': obj.subscription.plan.slug if obj.subscription.plan else 'starter',
                'status': obj.subscription.status,
                'billing_interval': obj.subscription.billing_interval,
                'price_monthly': obj.subscription.plan.price_monthly if obj.subscription.plan else 0,
                'payment_method': obj.subscription.payment_method,
                'features': obj.subscription.plan.features if obj.subscription.plan else [],
            }
        return None


class EmployerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    company = CompanySerializer(read_only=True)
    company_id = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all(), source='company', write_only=True, required=False
    )

    class Meta:
        model = EmployerProfile
        fields = ['id', 'user', 'company', 'company_id', 'designation', 'department', 'role_in_company', 'is_primary', 'created_at']
        read_only_fields = ['id', 'created_at']


class CompanyVerificationSerializer(serializers.ModelSerializer):
    company_name = serializers.ReadOnlyField(source='company.name')
    submitted_by_name = serializers.ReadOnlyField(source='submitted_by.get_full_name')

    class Meta:
        model = CompanyVerification
        fields = [
            'id', 'company', 'company_name', 'submitted_by', 'submitted_by_name',
            'trade_license_number', 'tax_id', 'official_document', 'official_document_url',
            'notes', 'status', 'admin_notes', 'reviewed_by', 'reviewed_at', 'created_at'
        ]
        read_only_fields = ['id', 'status', 'reviewed_by', 'reviewed_at', 'created_at']
