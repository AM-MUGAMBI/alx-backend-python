from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation
from .filters import MessageFilter
from .pagination import MessagePagination

class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [IsParticipantOfConversation]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['participants__email', 'conversation_id']
    ordering_fields = ['created_at']

    def get_queryset(self):
        # Return only conversations where the requesting user is a participant
        return Conversation.objects.filter(participants=self.request.user)

    def create(self, request, *args, **kwargs):
        participant_ids = request.data.get('participants', [])
        if not participant_ids or not isinstance(participant_ids, list):
            return Response({"error": "Participants list required."}, status=status.HTTP_400_BAD_REQUEST)

        participants = User.objects.filter(user_id__in=participant_ids)
        if participants.count() != len(participant_ids):
            return Response({"error": "Some participants not found."}, status=status.HTTP_400_BAD_REQUEST)

        # Include the requesting user if not already in participants
        if request.user not in participants:
            participants = list(participants) + [request.user]

        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        conversation.save()

        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsParticipantOfConversation]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = MessageFilter  # Custom filtering
    search_fields = ['sender__email', 'message_body']
    ordering_fields = ['sent_at']
    pagination_class = MessagePagination  # Pagination: 20 per page

    def get_queryset(self):
        # Only messages in conversations where the user is participant
        return Message.objects.filter(conversation__participants=self.request.user)

    def create(self, request, *args, **kwargs):
        sender = request.user
        conversation_id = request.data.get('conversation_id')
        message_body = request.data.get('message_body')

        if not conversation_id or not message_body:
            return Response({"error": "conversation_id and message_body are required."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            conversation = Conversation.objects.get(conversation_id=conversation_id)
        except Conversation.DoesNotExist:
            return Response({"error": "Conversation not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check if sender is participant
        if sender not in conversation.participants.all():
            return Response({"error": "You are not a participant in this conversation."},
                            status=status.HTTP_403_FORBIDDEN)

        message = Message.objects.create(sender=sender, conversation=conversation, message_body=message_body)
        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        message = self.get_object()
        if request.user not in message.conversation.participants.all():
            raise PermissionDenied("You do not have permission to update this message.")
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        message = self.get_object()
        if request.user not in message.conversation.participants.all():
            raise PermissionDenied("You do not have permission to delete this message.")
        return super().destroy(request, *args, **kwargs)
