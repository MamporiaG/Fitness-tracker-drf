# workouts/views.py

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import WorkoutSession
from .serializers import WorkoutSessionSerializer


class WorkoutSessionListCreateView(generics.ListCreateAPIView):
    serializer_class = WorkoutSessionSerializer

    def get_queryset(self):
        return (
            WorkoutSession.objects.filter(user=self.request.user)
            .prefetch_related("exercises__sets")
            .select_related("user")
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class WorkoutSessionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WorkoutSessionSerializer

    def get_queryset(self):
        return (
            WorkoutSession.objects.filter(user=self.request.user)
            .prefetch_related("exercises__sets")
            .select_related("user")
        )


class SessionsByDateView(generics.ListAPIView):
    serializer_class = WorkoutSessionSerializer

    def get_queryset(self):
        queryset = WorkoutSession.objects.filter(
            user=self.request.user
        ).prefetch_related("exercises__sets").select_related("user")

        session_date = self.request.query_params.get("date")
        if session_date:
            queryset = queryset.filter(date=session_date)
            
        return queryset