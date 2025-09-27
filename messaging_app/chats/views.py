from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer

class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['participants__email', 'conversation_id']
    ordering_fields = ['created_at']

    def get_queryset(self):
        # Return only conversations where the user is a participant
        return Conversation.objects.filter(participants=self.request.user)

    def create(self, request, *args, **kwargs):
        participant_ids = request.data.get('participants', [])
        if not participant_ids or not isinstance(participant_ids, list):
            return Response({"error": "Participants list required."}, status=status.HTTP_400_BAD_REQUEST)

        participants = User.objects.filter(user_id__in=participant_ids)
        if participants.count() != len(participant_ids):
            return Response({"error": "Some participants not found."}, status=status.HTTP_400_BAD_REQUEST)

        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        conversation.participants.add(request.user)  # Ensure creator is also added
        conversation.save()

        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['sender__email', 'message_body']
    ordering_fields = ['sent_at']

    def get_queryset(self):
        # Only show messages from conversations the user is in
        return Message.objects.filter(conversation__participants=self.request.user)

    def perform_create(self, serializer):
        """
        Automatically assign the logged-in user as the sender.
        """
        conversation_id = self.request.data.get('conversation_id')
        if not conversation_id:
            raise serializers.ValidationError({"error": "conversation_id is required."})

        try:
            conversation = Conversation.objects.get(conversation_id=conversation_id)
        except Conversation.DoesNotExist:
            raise serializers.ValidationError({"error": "Conversation not found."})

        if self.request.user not in conversation.participants.all():
            raise serializers.ValidationError({"error": "You are not a participant in this conversation."})

        serializer.save(sender=self.request.user, conversation=conversation)
