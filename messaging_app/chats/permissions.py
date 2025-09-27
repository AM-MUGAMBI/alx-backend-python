from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework import status
from rest_framework.response import Response
from .models import Conversation, Message


class IsParticipantOfConversation(BasePermission):
    """
    Custom permission to allow only participants of a conversation
    to view, send, update, or delete messages within that conversation.
    """

    def has_permission(self, request, view):
        # Check if user is authenticated
        if not request.user or not request.user.is_authenticated:
            return False

        # For list or create actions (POST, GET without pk)
        # Allow access, detailed object-level check will happen in has_object_permission
        if view.action in ['list', 'create']:
            return True

        # For retrieve, update, partial_update, destroy actions with object pk
        return True  # Let object-level permission handle this

    def has_object_permission(self, request, view, obj):
        user = request.user

        # Allow safe methods (GET, HEAD, OPTIONS) only if user is participant
        if request.method in SAFE_METHODS:
            return user in obj.participants.all() if hasattr(obj, 'participants') else user == obj.sender

        # For modifying methods, check that user is participant in conversation
        if request.method in ['PUT', 'PATCH', 'DELETE', 'POST']:
            # If obj is a Conversation, check participants
            if hasattr(obj, 'participants'):
                return user in obj.participants.all()

            # If obj is a Message, check participants via message.conversation
            if hasattr(obj, 'conversation'):
                return user in obj.conversation.participants.all()

        # Deny by default
        return False
