from django.urls import path
from apps.analytics.views import (
    EmployerAnalyticsView,
    CandidateDashboardView,
    AdminAnalyticsView,
    AdminExportCSVView
)

urlpatterns = [
    path('employer/', EmployerAnalyticsView.as_view(), name='analytics-employer'),
    path('candidate/', CandidateDashboardView.as_view(), name='analytics-candidate'),
    path('admin/', AdminAnalyticsView.as_view(), name='analytics-admin'),
    path('admin/export-csv/', AdminExportCSVView.as_view(), name='analytics-admin-export-csv'),
]
