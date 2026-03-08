# workouts/models.py

from django.db import models
from django.conf import settings
from exercises.models import Exercise


class WorkoutSession(models.Model):
    """
    Represents a full workout session.
    One session can contain multiple exercises.
    """
    user  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sessions')
    date  = models.DateField()
    notes = models.TextField(blank=True, default='')

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f'{self.user.username} — {self.date}'


class WorkoutExercise(models.Model):
    """
    Links an exercise to a session.
    One session can have many exercises
    """
    session  = models.ForeignKey(WorkoutSession, on_delete=models.CASCADE, related_name='exercises')
    exercise = models.ForeignKey(Exercise, on_delete=models.PROTECT, related_name='workout_exercises')

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'{self.exercise.name}'


class WorkoutSet(models.Model):
    """
    Represents a single set within a WorkoutExercise.
    """
    workout_exercise = models.ForeignKey(WorkoutExercise, on_delete=models.CASCADE, related_name='sets')
    set_number       = models.PositiveIntegerField()
    reps             = models.PositiveIntegerField()
    weight           = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        ordering = ['set_number']
        unique_together = ['workout_exercise', 'set_number']

    def __str__(self):
        return f'Set {self.set_number}: {self.reps} reps @ {self.weight}kg'