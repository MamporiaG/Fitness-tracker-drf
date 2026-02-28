from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    """
    - Any logged-in user can READ (GET) any session.
    - Only the owner can WRITE (PUT, PATCH, DELETE) their own sessions.
    """

    message = "You can only modify your own workout sessions."

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.user == request.user
