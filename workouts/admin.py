from django.contrib import admin
from .models import WorkoutSession, WorkoutExercise, WorkoutSet

admin.site.register(WorkoutSession)
admin.site.register(WorkoutExercise)
admin.site.register(WorkoutSet)