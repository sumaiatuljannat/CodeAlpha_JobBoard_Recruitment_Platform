from django.db import models
from apps.accounts.models import User

class Notification(models.Model):
    class NotificationType(models.TextChoices):
        APPLICATION_STATUS = 'application_status', 'Application Status'
        INTERVIEW_INVITE = 'interview_invite', 'Interview Invitation'
        NEW_APPLICATION = 'new_application', 'New Applicant'
        JOB_ALERT = 'job_alert', 'Job Alert'
        MESSAGE = 'message', 'New Message'
        RECOMMENDATION = 'recommendation', 'Job Recommendation'
        SYSTEM = 'system', 'System Notification'

    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=255)
    message = models.TextField()
    notification_type = models.CharField(max_length=30, choices=NotificationType.choices, default=NotificationType.SYSTEM)
    action_url = models.CharField(max_length=300, blank=True, default='')
    is_read = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Notification for {self.recipient.email}: {self.title}"


class NotificationPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='notification_preferences')
    email_application_updates = models.BooleanField(default=True)
    email_interviews = models.BooleanField(default=True)
    email_job_recommendations = models.BooleanField(default=True)
    email_messages = models.BooleanField(default=True)
    email_marketing = models.BooleanField(default=False)

    def __str__(self):
        return f"Preferences for {self.user.email}"
