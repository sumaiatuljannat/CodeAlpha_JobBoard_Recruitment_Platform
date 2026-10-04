from rest_framework import serializers
from apps.notifications.models import Notification, NotificationPreference

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'title', 'message', 'notification_type', 'action_url', 'is_read', 'created_at']
        read_only_fields = ['id', 'title', 'message', 'notification_type', 'action_url', 'created_at']


class NotificationPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationPreference
        fields = ['id', 'email_application_updates', 'email_interviews', 'email_job_recommendations', 'email_messages', 'email_marketing']
        read_only_fields = ['id']
