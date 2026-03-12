# exercises/serializers.py

from rest_framework import serializers
from .models import Exercise


class ExerciseSerializer(serializers.ModelSerializer):
    muscle_group = serializers.ChoiceField(choices=Exercise.MuscleGroup.choices)

    class Meta:
        model = Exercise
        fields = (
            "id",
            "owner",
            "name",
            "muscle_group",
        )
        read_only_fields = ["owner"]
