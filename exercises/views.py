# exercises/views.py

from rest_framework import generics
from rest_framework.permissions import SAFE_METHODS, BasePermission

from .models import Exercise
from .serializers import ExerciseSerializer


class IsOwnerAdminOrReadOnly(BasePermission):
    """
    - All authenticated users can read (GET) and create (POST).
    - Only the owner or an Admin can edit/delete (PUT/PATCH/DELETE).
    """

    def has_permission(self, request, view):
        """
        View level permission for all request - GET, POST, PUT, DELETE
        """
        if request.user and request.user.is_authenticated:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        """
        Object-level permission for detail views (GET, PUT, DELETE)
        Authenticated/logged in users can read the objects
        To edit or delete the object, user must be the object owner or an admin
        """

        if request.method in SAFE_METHODS:
            return True

        if request.user.is_staff or obj.owner == request.user:
            return True

        return False


class ExerciseListCreateView(generics.ListCreateAPIView):
    serializer_class = ExerciseSerializer
    permission_classes = (IsOwnerAdminOrReadOnly,)

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Exercise.objects.all()

        return Exercise.objects.filter(owner=user)

    def perform_create(self, serializer):
        """
        Owner gets automatically assigned by the server
        """
        serializer.save(owner=self.request.user)


class ExerciseDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ExerciseSerializer
    permission_classes = (IsOwnerAdminOrReadOnly,)

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Exercise.objects.all()

        return Exercise.objects.filter(owner=user)
