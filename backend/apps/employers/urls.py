from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.employers.views import (
    CompanyViewSet,
    CompanyVerificationViewSet,
    SubscriptionPlanViewSet,
    CompanySubscriptionViewSet,
    CompanyTeamViewSet
)

router = DefaultRouter()
router.register(r'companies', CompanyViewSet, basename='companies')
router.register(r'verifications', CompanyVerificationViewSet, basename='verifications')
router.register(r'plans', SubscriptionPlanViewSet, basename='plans')
router.register(r'subscription', CompanySubscriptionViewSet, basename='subscription')
router.register(r'team', CompanyTeamViewSet, basename='team')

urlpatterns = [
    path('', include(router.urls)),
]
