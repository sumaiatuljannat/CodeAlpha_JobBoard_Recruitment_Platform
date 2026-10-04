from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.jobs.views import JobCategoryViewSet, SkillViewSet, JobViewSet, JobReportViewSet

router = DefaultRouter()
router.register(r'categories', JobCategoryViewSet, basename='job-categories')
router.register(r'skills', SkillViewSet, basename='skills')
router.register(r'reports', JobReportViewSet, basename='job-reports')
router.register(r'listings', JobViewSet, basename='jobs')

urlpatterns = [
    path('', include(router.urls)),
]
