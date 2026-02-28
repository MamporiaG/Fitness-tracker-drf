# workouts/models.py

from django.db import models
from django.contrib.auth.models import User
from exercises.models import Exercise


class WorkoutSession(models.Model):
    # CASCADE - if user is deleted, their sessions must be deleted as well.
    user     = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
    # PROTECT means: you cannot delete an exercise that has sessions logged against it
    exercise = models.ForeignKey(Exercise, on_delete=models.PROTECT, related_name='sessions')
    date     = models.DateField()
    sets     = models.PositiveIntegerField(help_text='Number of sets performed')
    reps     = models.PositiveIntegerField(help_text='Reps per set')
    weight   = models.DecimalField(max_digits=6, decimal_places=2, help_text='Weight in kg')
    notes    = models.TextField(blank=True, default='')

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f'{self.user.username} — {self.exercise.name} on {self.date}'

