from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from apps.accounts.models import User, AuditLog

class UserSerializer(serializers.ModelSerializer):
    display_avatar = serializers.ReadOnlyField()
    candidate_profile_id = serializers.SerializerMethodField()
    employer_company_id = serializers.SerializerMethodField()
    company_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name', 'role',
            'phone', 'avatar', 'avatar_url', 'display_avatar', 'bio',
            'is_email_verified', 'is_active', 'created_at',
            'candidate_profile_id', 'employer_company_id', 'company_name'
        ]
        read_only_fields = ['id', 'created_at', 'is_email_verified']

    def get_candidate_profile_id(self, obj):
        if hasattr(obj, 'candidate_profile'):
            return obj.candidate_profile.id
        return None

    def get_employer_company_id(self, obj):
        if hasattr(obj, 'employer_profile'):
            return obj.employer_profile.company.id
        return None

    def get_company_name(self, obj):
        if hasattr(obj, 'employer_profile'):
            return obj.employer_profile.company.name
        return None


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    company_name = serializers.CharField(write_only=True, required=False, allow_blank=True)
    company_industry = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'first_name', 'last_name', 'role', 'phone', 'company_name', 'company_industry']

    def create(self, validated_data):
        password = validated_data.pop('password')
        company_name = validated_data.pop('company_name', '')
        company_industry = validated_data.pop('company_industry', 'Technology')
        
        user = User.objects.create_user(
            password=password,
            **validated_data
        )

        # Auto-create related profiles depending on role
        if user.role == User.Role.CANDIDATE:
            from apps.candidates.models import CandidateProfile
            CandidateProfile.objects.create(
                user=user,
                headline=f"{user.first_name} {user.last_name} | Professional"
            )
        elif user.role == User.Role.EMPLOYER:
            from apps.employers.models import Company, EmployerProfile
            c_name = company_name.strip() if company_name else f"{user.last_name or user.first_name}'s Organization"
            company, _ = Company.objects.get_or_create(
                name=c_name,
                defaults={
                    'industry': company_industry or 'Information Technology',
                    'headquarters': 'Remote / Global',
                    'about': f"Welcome to {c_name}. We are building high-impact technology and hiring top talent.",
                }
            )
            EmployerProfile.objects.create(
                user=user,
                company=company,
                designation='Recruitment Lead',
                is_primary=True
            )

        from apps.notifications.models import NotificationPreference
        NotificationPreference.objects.get_or_create(user=user)

        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email', '').strip().lower()
        password = attrs.get('password')

        user = authenticate(username=email, password=password)
        if not user:
            # Check if user exists but inactive
            user_exists = User.objects.filter(email=email).first()
            if user_exists and not user_exists.is_active:
                raise serializers.ValidationError('Your account is currently inactive or suspended.')
            raise serializers.ValidationError('Invalid email or password.')

        refresh = RefreshToken.for_user(user)
        return {
            'user': user,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=6)


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class PasswordResetConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    token = serializers.CharField(required=False, default='demo-reset-code')
    new_password = serializers.CharField(required=True, min_length=6)


class AuditLogSerializer(serializers.ModelSerializer):
    user_email = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = AuditLog
        fields = ['id', 'user', 'user_email', 'action', 'ip_address', 'user_agent', 'details', 'created_at']
