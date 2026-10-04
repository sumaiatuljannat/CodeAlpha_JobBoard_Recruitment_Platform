from django.db import models
from apps.accounts.models import User
from apps.jobs.models import Job

class Conversation(models.Model):
    job = models.ForeignKey(Job, on_delete=models.SET_NULL, null=True, blank=True, related_name='conversations')
    employer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='employer_conversations')
    candidate = models.ForeignKey(User, on_delete=models.CASCADE, related_name='candidate_conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"Conversation: {self.employer.get_full_name()} & {self.candidate.get_full_name()}"


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    is_read = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Message by {self.sender.get_full_name()} at {self.created_at}"
