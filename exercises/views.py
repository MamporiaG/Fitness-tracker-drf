# exercises/views.py

from rest_framework import generics
from .models import Exercise
from .serializers import ExerciseSerializer

class ExerciseListCreateView(generics.ListCreateAPIView):
    serializer_class = ExerciseSerializer

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

    def get_queryset(self):
        user = self.request.user
        
        if user.is_staff:
            return Exercise.objects.all()
            
        return Exercise.objects.filter(owner=user)