from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.candidates.views import (
    CandidateProfileViewSet,
    EducationViewSet,
    ExperienceViewSet,
    CandidateSkillViewSet,
    ProjectViewSet,
    CertificationViewSet,
    ResumeViewSet,
    ResumeBuilderViewSet,
    SavedJobViewSet,
    JobAlertViewSet
)

router = DefaultRouter()
router.register(r'profiles', CandidateProfileViewSet, basename='candidate-profiles')
router.register(r'educations', EducationViewSet, basename='candidate-educations')
router.register(r'experiences', ExperienceViewSet, basename='candidate-experiences')
router.register(r'skills', CandidateSkillViewSet, basename='candidate-skills')
router.register(r'projects', ProjectViewSet, basename='candidate-projects')
router.register(r'certifications', CertificationViewSet, basename='candidate-certifications')
router.register(r'resumes', ResumeViewSet, basename='candidate-resumes')
router.register(r'resume-builder', ResumeBuilderViewSet, basename='resume-builder')
router.register(r'saved-jobs', SavedJobViewSet, basename='saved-jobs')
router.register(r'alerts', JobAlertViewSet, basename='job-alerts')

urlpatterns = [
    path('', include(router.urls)),
]
