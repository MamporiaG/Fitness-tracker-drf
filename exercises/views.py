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
        # 1. View-level permission: Must be logged in to access the endpoints at all.
        # This allows GET (list) and POST (create) for authenticated users.
        if request.user and request.user.is_authenticated:
            return True

        return False


    def has_object_permission(self, request, view, obj):
        # 2. Object-level permission: Only runs on detail views (PUT, DELETE, single GET).

        # Anyone authenticated can read the specific object
        if request.method in SAFE_METHODS:
            return True

        # To modify or delete, the user must be an admin OR the owner of the object
        if request.user.is_staff or obj.owner == request.user:
            return True

        return False


class ExerciseListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/exercises/  → list all exercises
    POST /api/exercises/  → create a new exercise (any authenticated user)
    """

    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = (IsOwnerAdminOrReadOnly,)

    def perform_create(self, serializer):
        # Automatically assign the logged-in user as the owner of the exercise
        serializer.save(owner=self.request.user)


class ExerciseDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/exercises/{id}/  → get one exercise (any authenticated user)
    PUT    /api/exercises/{id}/  → update (owner or admin only)
    DELETE /api/exercises/{id}/  → delete (owner or admin only)
    """

    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = (IsOwnerAdminOrReadOnly,)
