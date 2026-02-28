from django.urls import path
from .views import WorkoutSessionListCreateView, WorkoutSessionDetailView, MySessionsView

urlpatterns = [
    path('sessions/',           WorkoutSessionListCreateView.as_view(), name='session-list'),
    path('sessions/mine/',      MySessionsView.as_view(),               name='session-mine'),
    path('sessions/<int:pk>/',  WorkoutSessionDetailView.as_view(),     name='session-detail'),
]
