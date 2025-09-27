from rest_framework.permissions import BasePermission

class IsParticipantOfConversation(BasePermission):
    """
    Custom permission:
    - Only authenticated users can access
    - Only participants of the conversation can view, update, delete messages or conversations
    """

    def has_permission(self, request, view):
        # Allow only authenticated users
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user

        # For Conversation objects
        if hasattr(obj, 'participants'):
            return user in obj.participants.all()

        # For Message objects
        if hasattr(obj, 'conversation'):
            return user in obj.conversation.participants.all()

        return False
