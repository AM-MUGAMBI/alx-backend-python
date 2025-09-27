from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow users to access their own objects.
    """

    def has_object_permission(self, request, view, obj):
        # Assumes the object has an `owner` or `user` attribute
        return obj.user == request.user or obj.owner == request.user

