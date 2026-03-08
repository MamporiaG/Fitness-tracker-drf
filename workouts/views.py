# workouts/views.py

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import WorkoutSession
from .serializers import WorkoutSessionSerializer
from .permissions import IsOwnerOrReadOnly


class WorkoutSessionListCreateView(generics.ListCreateAPIView):
    serializer_class = WorkoutSessionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            WorkoutSession.objects.prefetch_related("exercises__sets")
            .select_related("user")
            .all()
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class WorkoutSessionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WorkoutSessionSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        return (
            WorkoutSession.objects.prefetch_related("exercises__sets")
            .select_related("user")
            .all()
        )


class MySessionsView(generics.ListAPIView):
    serializer_class = WorkoutSessionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return WorkoutSession.objects.filter(user=self.request.user).prefetch_related(
            "exercises__sets"
        )


class SessionsByDateView(generics.ListAPIView):
    serializer_class = WorkoutSessionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = WorkoutSession.objects.filter(
            user=self.request.user
        ).prefetch_related("exercises__sets")

        session_date = self.request.query_params.get("date")
        if session_date:
            queryset = queryset.filter(date=session_date)

        return queryset
