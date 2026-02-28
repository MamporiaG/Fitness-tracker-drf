from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import WorkoutSession
from .serializers import WorkoutSessionSerializer
from .permissions import IsOwnerOrReadOnly


class WorkoutSessionListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/sessions/  → list all sessions (everyone's, read-only for non-owners)
    POST /api/sessions/  → create a new session (logged-in users only)
    """
    serializer_class   = WorkoutSessionSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        # Return all sessions — any logged-in user can read
        return WorkoutSession.objects.select_related('user', 'exercise').all()

    def perform_create(self, serializer):
        # Automatically set the logged-in user as the owner
        # The client never sends 'user' — we inject it here
        serializer.save(user=self.request.user)


class WorkoutSessionDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/sessions/{id}/  → view a session (anyone logged in)
    PUT    /api/sessions/{id}/  → replace a session (owner only)
    PATCH  /api/sessions/{id}/  → partially update a session (owner only)
    DELETE /api/sessions/{id}/  → delete a session (owner only)
    """
    serializer_class   = WorkoutSessionSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    queryset           = WorkoutSession.objects.select_related('user', 'exercise').all()


class MySessionsView(generics.ListAPIView):
    """
    GET /api/sessions/mine/  → list only YOUR sessions
    """
    serializer_class   = WorkoutSessionSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return WorkoutSession.objects.filter(user=self.request.user).select_related('exercise')
