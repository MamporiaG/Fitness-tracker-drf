# workouts/urls.py
from django.urls import path
from .views import (
    WorkoutSessionListCreateView,
    WorkoutSessionDetailView,
    SessionsByDateView,
)

urlpatterns = [
    path("sessions/", WorkoutSessionListCreateView.as_view(), name="session-list"),
    path(
        "sessions/<int:pk>/", WorkoutSessionDetailView.as_view(), name="session-detail"
    ),
    path("sessions/by-date/", SessionsByDateView.as_view(), name="sessions-by-date"),
]
