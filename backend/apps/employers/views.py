from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from apps.employers.models import (
    Company,
    EmployerProfile,
    CompanyVerification,
    SubscriptionPlan,
    CompanySubscription
)
from apps.employers.serializers import (
    CompanySerializer,
    EmployerProfileSerializer,
    CompanyVerificationSerializer,
    SubscriptionPlanSerializer,
    CompanySubscriptionSerializer
)
from apps.accounts.permissions import IsEmployer, IsAdminUserRole

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all().prefetch_related('jobs')
    serializer_class = CompanySerializer
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['industry', 'company_size', 'is_verified', 'is_featured']
    search_fields = ['name', 'industry', 'headquarters', 'about']
    ordering_fields = ['name', 'created_at']

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'featured']:
            return [permissions.AllowAny()]
        if self.action in ['create', 'update', 'partial_update']:
            return [permissions.IsAuthenticated()]
        return [IsAdminUserRole()]

    @action(detail=False, methods=['get'])
    def featured(self, request):
        featured_companies = self.queryset.filter(is_featured=True)[:8]
        serializer = self.get_serializer(featured_companies, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsEmployer])
    def my_company(self, request):
        if not hasattr(request.user, 'employer_profile'):
            return Response({'detail': 'No employer profile found.'}, status=status.HTTP_404_NOT_FOUND)
        company = request.user.employer_profile.company
        serializer = self.get_serializer(company)
        return Response(serializer.data)


class CompanyVerificationViewSet(viewsets.ModelViewSet):
    serializer_class = CompanyVerificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin' or user.is_staff:
            return CompanyVerification.objects.all()
        if hasattr(user, 'employer_profile'):
            return CompanyVerification.objects.filter(company=user.employer_profile.company)
        return CompanyVerification.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        if not hasattr(user, 'employer_profile'):
            raise permissions.exceptions.PermissionDenied("Must be an employer to request verification.")
        
        company = user.employer_profile.company
        company.verification_status = Company.VerificationStatus.PENDING
        company.save(update_fields=['verification_status'])
        
        serializer.save(
            company=company,
            submitted_by=user,
            status=Company.VerificationStatus.PENDING
        )

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUserRole])
    def approve(self, request, pk=None):
        verification = self.get_object()
        verification.status = Company.VerificationStatus.VERIFIED
        verification.reviewed_by = request.user
        verification.reviewed_at = timezone.now()
        verification.admin_notes = request.data.get('admin_notes', 'Approved by administrator.')
        verification.save()

        # Update company badge
        company = verification.company
        company.is_verified = True
        company.verification_status = Company.VerificationStatus.VERIFIED
        company.save()

        return Response({'success': True, 'message': f'{company.name} verified successfully.'})

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUserRole])
    def reject(self, request, pk=None):
        verification = self.get_object()
        verification.status = Company.VerificationStatus.REJECTED
        verification.reviewed_by = request.user
        verification.reviewed_at = timezone.now()
        verification.admin_notes = request.data.get('admin_notes', 'Verification rejected.')
        verification.save()

        company = verification.company
        company.is_verified = False
        return Response({'success': True, 'message': f'{company.name} verification rejected.'})


class SubscriptionPlanViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SubscriptionPlan.objects.all().order_by('price_monthly')
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [permissions.AllowAny]


class CompanySubscriptionViewSet(viewsets.ViewSet):
    permission_classes = [IsEmployer]

    @action(detail=False, methods=['get'])
    def my(self, request):
        if not hasattr(request.user, 'employer_profile'):
            return Response({'detail': 'Employer profile required.'}, status=status.HTTP_404_NOT_FOUND)
        company = request.user.employer_profile.company
        sub, _ = CompanySubscription.objects.get_or_create(
            company=company,
            defaults={
                'status': 'active',
                'billing_interval': 'monthly',
                'payment_method': 'Commercial B2B Invoicing (Net 30)'
            }
        )
        if not sub.plan:
            sub.plan = SubscriptionPlan.objects.filter(slug='growth' if company.is_verified else 'starter').first()
            sub.save()
        return Response(CompanySubscriptionSerializer(sub).data)

    @action(detail=False, methods=['post'])
    def upgrade(self, request):
        if not hasattr(request.user, 'employer_profile'):
            return Response({'detail': 'Employer profile required.'}, status=status.HTTP_404_NOT_FOUND)
        company = request.user.employer_profile.company
        plan_id = request.data.get('plan_id')
        billing_interval = request.data.get('billing_interval', 'monthly')

        plan = SubscriptionPlan.objects.filter(pk=plan_id).first()
        if not plan:
            return Response({'detail': 'Invalid plan selected.'}, status=status.HTTP_400_BAD_REQUEST)

        sub, _ = CompanySubscription.objects.get_or_create(company=company)
        sub.plan = plan
        sub.billing_interval = billing_interval
        sub.status = CompanySubscription.Status.ACTIVE
        sub.current_period_start = timezone.now()
        sub.current_period_end = timezone.now() + timezone.timedelta(days=365 if billing_interval == 'yearly' else 30)
        sub.save()

        return Response({
            'success': True,
            'message': f'Company subscription updated to {plan.name} ({billing_interval}).',
            'subscription': CompanySubscriptionSerializer(sub).data
        })

    @action(detail=False, methods=['post'])
    def cancel(self, request):
        if not hasattr(request.user, 'employer_profile'):
            return Response({'detail': 'Employer profile required.'}, status=status.HTTP_404_NOT_FOUND)
        company = request.user.employer_profile.company
        sub = CompanySubscription.objects.filter(company=company).first()
        if sub:
            sub.auto_renew = False
            sub.save(update_fields=['auto_renew'])
        return Response({'success': True, 'message': 'Auto-renewal turned off for subscription.'})


class CompanyTeamViewSet(viewsets.ViewSet):
    permission_classes = [IsEmployer]

    def list(self, request):
        if not hasattr(request.user, 'employer_profile'):
            return Response({'detail': 'Employer profile required.'}, status=status.HTTP_404_NOT_FOUND)
        company = request.user.employer_profile.company
        team = EmployerProfile.objects.filter(company=company).select_related('user')
        return Response({
            'success': True,
            'company': company.name,
            'team': EmployerProfileSerializer(team, many=True).data
        })

    @action(detail=False, methods=['post'])
    def invite(self, request):
        if not hasattr(request.user, 'employer_profile'):
            return Response({'detail': 'Employer profile required.'}, status=status.HTTP_404_NOT_FOUND)
        company = request.user.employer_profile.company
        email = request.data.get('email', '').strip().lower()
        role = request.data.get('role', 'recruiter')
        designation = request.data.get('designation', 'Recruitment Specialist')
        first_name = request.data.get('first_name', 'Colleague')
        last_name = request.data.get('last_name', '')

        if not email:
            return Response({'detail': 'Email is required.'}, status=status.HTTP_400_BAD_REQUEST)

        from apps.accounts.models import User
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'first_name': first_name,
                'last_name': last_name,
                'role': User.Role.EMPLOYER,
                'is_active': True,
                'is_email_verified': True
            }
        )
        if created:
            user.set_password('demo123456')
            user.save()

        profile, p_created = EmployerProfile.objects.get_or_create(
            user=user,
            defaults={
                'company': company,
                'designation': designation,
                'role_in_company': role,
                'is_primary': False
            }
        )
        if not p_created:
            profile.company = company
            profile.role_in_company = role
            profile.designation = designation
            profile.save()

        return Response({
            'success': True,
            'message': f'Team member {email} added successfully with role {role}.',
            'member': EmployerProfileSerializer(profile).data
        })
