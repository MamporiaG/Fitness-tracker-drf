from rest_framework import serializers
from .models import WorkoutSession


class WorkoutSessionSerializer(serializers.ModelSerializer):
    owner         = serializers.CharField(source='user.username', read_only=True)
    exercise_name = serializers.CharField(source='exercise.name', read_only=True)

    class Meta:
        model  = WorkoutSession
        fields = (
            'id',
            'owner',          
            'exercise',       
            'exercise_name',  
            'date',
            'sets',
            'reps',
            'weight',
            'notes',
        )
        read_only_fields = ('owner', 'exercise_name')
