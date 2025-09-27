from rest_framework.permissions import BasePermission, IsAuthenticated
from .models import Conversation, Message

class IsParticipantOfConversation(IsAuthenticated):
    """
    Allows access only to authenticated users who are participants
    of the conversation associated with the object.
    """

    def has_permission(self, request, view):
        # Ensure user is authenticated first
        if not super().has_permission(request, view):
            return False

        # For list and create actions, allow if authenticated (detail check in has_object_permission)
        return True

    def has_object_permission(self, request, view, obj):
        user = request.user

        # If object is a Conversation, check if user is participant
        if isinstance(obj, Conversation):
            return user in obj.participants.all()

        # If object is a Message, check if user is participant in message's conversation
        if isinstance(obj, Message):
            return user in obj.conversation.participants.all()

        # Default deny
        return False
