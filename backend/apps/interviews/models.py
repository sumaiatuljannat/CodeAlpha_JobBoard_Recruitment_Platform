from django.db import models
from apps.accounts.models import User
from apps.applications.models import JobApplication

class Interview(models.Model):
    class InterviewType(models.TextChoices):
        ONLINE = 'online', 'Online / Video Call'
        PHONE = 'phone', 'Phone Screening'
        IN_PERSON = 'in_person', 'In-Person'

    class Status(models.TextChoices):
        SCHEDULED = 'scheduled', 'Scheduled'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'
        RESCHEDULED = 'rescheduled', 'Rescheduled'

    application = models.ForeignKey(JobApplication, on_delete=models.CASCADE, related_name='interviews')
    interviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conducted_interviews')
    title = models.CharField(max_length=255, default='Technical Interview')
    interview_type = models.CharField(max_length=30, choices=InterviewType.choices, default=InterviewType.ONLINE)
    scheduled_at = models.DateTimeField(db_index=True)
    duration_minutes = models.PositiveIntegerField(default=45)
    meeting_link = models.URLField(max_length=500, blank=True)
    location = models.CharField(max_length=255, blank=True)
    instructions = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.SCHEDULED, db_index=True)
    candidate_feedback = models.TextField(blank=True)
    internal_notes = models.TextField(blank=True)
    rating = models.PositiveIntegerField(null=True, blank=True)  # 1 to 5
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['scheduled_at']

    def __str__(self):
        return f"{self.title} for {self.application.candidate.user.get_full_name()} ({self.status})"
