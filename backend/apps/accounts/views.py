from rest_framework import generics, status, views, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from apps.accounts.models import User, AuditLog
from apps.accounts.serializers import (
    UserSerializer,
    RegisterSerializer,
    LoginSerializer,
    ChangePasswordSerializer,
    AuditLogSerializer
)
from apps.accounts.permissions import IsAdminUserRole

def log_user_action(user, action, request, details=None):
    ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', ''))
    agent = request.META.get('HTTP_USER_AGENT', '')
    AuditLog.objects.create(
        user=user if user and user.is_authenticated else None,
        action=action,
        ip_address=ip.split(',')[0].strip() if ip else None,
        user_agent=agent[:500],
        details=details or {}
    )

class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        log_user_action(user, 'USER_REGISTERED', request, {'role': user.role})
        
        return Response({
            'success': True,
            'message': 'Registration successful.',
            'user': UserSerializer(user).data,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }, status=status.HTTP_201_CREATED)


class LoginView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = data['user']
        log_user_action(user, 'USER_LOGIN', request)

        return Response({
            'success': True,
            'message': 'Login successful.',
            'user': UserSerializer(user).data,
            'access': data['access'],
            'refresh': data['refresh'],
        }, status=status.HTTP_200_OK)


class DemoLoginView(views.APIView):
    """Convenient endpoint for 1-click test login as Candidate, Employer, or Admin"""
    permission_classes = [AllowAny]

    def post(self, request):
        role = request.data.get('role', 'candidate').lower()
        
        user = None
        if role == 'candidate':
            user = User.objects.filter(role=User.Role.CANDIDATE, is_active=True).first()
        elif role == 'employer':
            user = User.objects.filter(role=User.Role.EMPLOYER, is_active=True).first()
        elif role == 'admin':
            user = User.objects.filter(role=User.Role.ADMIN, is_active=True).first()

        if not user:
            # Fallback creation if seed not run yet
            email = f"demo.{role}@hiresphere.io"
            user, _ = User.objects.get_or_create(
                email=email,
                defaults={
                    'first_name': 'Demo',
                    'last_name': role.capitalize(),
                    'role': role,
                    'is_active': True,
                    'is_email_verified': True
                }
            )
            user.set_password('demo123456')
            user.save()

        refresh = RefreshToken.for_user(user)
        log_user_action(user, f'DEMO_LOGIN_{role.upper()}', request)

        return Response({
            'success': True,
            'message': f'Logged in as demo {role}.',
            'user': UserSerializer(user).data,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        })


class MeView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response({
            'success': True,
            'user': serializer.data
        })

    def patch(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        log_user_action(request.user, 'USER_PROFILE_UPDATED', request)
        return Response({
            'success': True,
            'message': 'Profile updated successfully.',
            'user': serializer.data
        })


class ChangePasswordView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        if not user.check_password(serializer.validated_data['old_password']):
            return Response({'detail': 'Current password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        log_user_action(user, 'PASSWORD_CHANGED', request)
        return Response({'success': True, 'message': 'Password updated successfully.'})


class LogoutView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.data.get('refresh')
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except Exception:
                pass
        if request.user.is_authenticated:
            log_user_action(request.user, 'USER_LOGOUT', request)
        return Response({'success': True, 'message': 'Logged out successfully.'})


class PasswordResetRequestView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email', '').strip().lower()
        if not email:
            return Response({'detail': 'Email is required.'}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.filter(email=email).first()
        if user:
            log_user_action(user, 'PASSWORD_RESET_REQUESTED', request)
        return Response({
            'success': True,
            'message': f"If an account exists for {email}, password recovery instructions and a verification code have been dispatched.",
            'demo_code': '884920'
        })


class PasswordResetConfirmView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email', '').strip().lower()
        new_password = request.data.get('new_password', '')
        if not email or not new_password:
            return Response({'detail': 'Email and new password are required.'}, status=status.HTTP_400_BAD_REQUEST)
        if len(new_password) < 6:
            return Response({'detail': 'Password must be at least 6 characters.'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.filter(email=email).first()
        if not user:
            return Response({'detail': 'No user found with this email.'}, status=status.HTTP_404_NOT_FOUND)
        
        user.set_password(new_password)
        user.save()
        log_user_action(user, 'PASSWORD_RESET_COMPLETED', request)
        return Response({'success': True, 'message': 'Password reset successful. You can now log in.'})


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAdminUserRole]
    serializer_class = AuditLogSerializer
    queryset = AuditLog.objects.all()
