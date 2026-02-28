# exercises/serializers.py

from rest_framework import serializers
from .models import Exercise


class ExerciseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Exercise
        fields = (
            "id",
            "owner"
            "name",
            "muscle_group",
        )
        read_only_fields = ["owner"]
