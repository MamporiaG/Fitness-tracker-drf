# exercies/models.py

from django.db import models
from django.conf import settings


class Exercise(models.Model):

    class MuscleGroup(models.TextChoices):
        CHEST = "chest"
        BACK = "back"
        SHOULDERS = "shoulders"
        BICEPS = "biceps"
        TRICEPS = "triceps"
        CORE = "core"
        QUADRICEPS = "quadriceps"
        HAMSTRINGS = "hamstrings"
        GLUTES = "glutes"
        CALVES = "calves"

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="exercises"
    )

    name = models.CharField(max_length=100)

    muscle_group = models.CharField(
        max_length=20,
        choices=MuscleGroup.choices,
    )

    class Meta:
        ordering = ["muscle_group", "name"]

    def __str__(self):
        return self.name
