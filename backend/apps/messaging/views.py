from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from apps.messaging.models import Conversation, Message
from apps.messaging.serializers import ConversationSerializer, MessageSerializer
from apps.notifications.models import Notification

class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Conversation.objects.filter(
            Q(employer=user) | Q(candidate=user)
        ).select_related('employer', 'candidate', 'job').prefetch_related('messages')

    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        conversation = self.get_object()
        # Mark other person's messages as read
        conversation.messages.filter(is_read=False).exclude(sender=request.user).update(is_read=True)
        
        messages = conversation.messages.all()
        serializer = MessageSerializer(messages, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
        conversation = self.get_object()
        content = request.data.get('content', '').strip()
        if not content:
            return Response({'detail': 'Message content cannot be empty.'}, status=status.HTTP_400_BAD_REQUEST)

        msg = Message.objects.create(
            conversation=conversation,
            sender=request.user,
            content=content
        )
        conversation.save()  # update timestamp

        # Notify recipient
        recipient = conversation.candidate if request.user == conversation.employer else conversation.employer
        Notification.objects.create(
            recipient=recipient,
            title=f"New message from {request.user.get_full_name()}",
            message=content[:100],
            notification_type=Notification.NotificationType.MESSAGE,
            action_url="/messages"
        )

        return Response(MessageSerializer(msg, context={'request': request}).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def start_or_get(self, request):
        candidate_id = request.data.get('candidate_id')
        employer_id = request.data.get('employer_id')
        job_id = request.data.get('job_id')

        user = request.user
        if user.role == 'candidate':
            cand_user = user
            emp_id = employer_id
        else:
            cand_id = candidate_id
            cand_user = None
            from apps.accounts.models import User
            if cand_id:
                cand_user = User.objects.filter(id=cand_id).first()
            emp_id = user.id

        if not cand_user or not emp_id:
            return Response({'detail': 'Both candidate and employer must be specified.'}, status=status.HTTP_400_BAD_REQUEST)

        from apps.accounts.models import User
        emp_user = User.objects.get(id=emp_id)

        conv = Conversation.objects.filter(
            employer=emp_user,
            candidate=cand_user,
            job_id=job_id
        ).first()

        if not conv:
            conv = Conversation.objects.create(
                employer=emp_user,
                candidate=cand_user,
                job_id=job_id
            )

        return Response(ConversationSerializer(conv, context={'request': request}).data)
