from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.applications.views import JobApplicationViewSet

router = DefaultRouter()
router.register(r'', JobApplicationViewSet, basename='applications')

urlpatterns = [
    path('', include(router.urls)),
]
