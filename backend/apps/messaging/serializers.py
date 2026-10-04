from rest_framework import serializers
from apps.messaging.models import Conversation, Message
from apps.accounts.serializers import UserSerializer
from apps.jobs.serializers import JobSerializer

class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.ReadOnlyField(source='sender.get_full_name')
    sender_avatar = serializers.ReadOnlyField(source='sender.display_avatar')
    is_me = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['id', 'conversation', 'sender', 'sender_name', 'sender_avatar', 'content', 'is_read', 'is_me', 'created_at']
        read_only_fields = ['id', 'sender', 'is_read', 'created_at']

    def get_is_me(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.sender == request.user
        return False


class ConversationSerializer(serializers.ModelSerializer):
    employer_details = UserSerializer(source='employer', read_only=True)
    candidate_details = UserSerializer(source='candidate', read_only=True)
    job_details = JobSerializer(source='job', read_only=True)
    last_message = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = [
            'id', 'job', 'job_details', 'employer', 'employer_details',
            'candidate', 'candidate_details', 'last_message', 'unread_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_last_message(self, obj):
        msg = obj.messages.last()
        if msg:
            return MessageSerializer(msg, context=self.context).data
        return None

    def get_unread_count(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.messages.filter(is_read=False).exclude(sender=request.user).count()
        return 0
