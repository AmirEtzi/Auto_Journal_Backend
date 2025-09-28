from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwner(BasePermission):
    """Allow access only to objects owned by the requesting user."""

    def has_object_permission(self, request, view, obj):
        return getattr(obj, 'user_id', None) == getattr(request.user, 'id', None)


