# workouts/serializers.py

from rest_framework import serializers
from .models import WorkoutSession, WorkoutExercise, WorkoutSet


class WorkoutSetSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = WorkoutSet
        fields = ("id", "set_number", "reps", "weight")


class WorkoutExerciseSerializer(serializers.ModelSerializer):
    """Sets are nested inside exercises"""

    id = serializers.IntegerField(required=False)
    sets = WorkoutSetSerializer(many=True)

    class Meta:
        model = WorkoutExercise
        fields = ("id", "exercise", "sets")


class WorkoutSessionSerializer(serializers.ModelSerializer):
    """Exercises are nested inside workout sessions"""

    owner = serializers.CharField(source="user.username", read_only=True)
    exercises = WorkoutExerciseSerializer(many=True)

    class Meta:
        model = WorkoutSession
        fields = ("id", "owner", "date", "notes", "exercises")
        read_only_fields = ("owner",)

    def create(self, validated_data):
        exercises_data = validated_data.pop("exercises")

        session = WorkoutSession.objects.create(**validated_data)

        for exercise_data in exercises_data:
            sets_data = exercise_data.pop("sets")

            workout_exercise = WorkoutExercise.objects.create(
                session=session, **exercise_data
            )

            for set_data in sets_data:
                WorkoutSet.objects.create(workout_exercise=workout_exercise, **set_data)

        return session

    def update(self, instance, validated_data):
        exercises_data = validated_data.pop("exercises", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if exercises_data is not None:
            incoming_exercise_ids = [
                item["id"] for item in exercises_data if "id" in item
            ]

            instance.exercises.exclude(id__in=incoming_exercise_ids).delete()

            for exercise_data in exercises_data:
                sets_data = exercise_data.pop("sets", None)
                exercise_id = exercise_data.get("id", None)

                if exercise_id:
                    workout_exercise = WorkoutExercise.objects.get(
                        id=exercise_id, session=instance
                    )
                    workout_exercise.exercise_id = exercise_data.get(
                        "exercise", workout_exercise.exercise_id
                    )
                    workout_exercise.save()
                else:
                    workout_exercise = WorkoutExercise.objects.create(
                        session=instance, **exercise_data
                    )

                if sets_data is not None:
                    incoming_set_ids = [
                        item["id"] for item in sets_data if "id" in item
                    ]

                    workout_exercise.sets.exclude(id__in=incoming_set_ids).delete()

                    for set_data in sets_data:
                        set_id = set_data.get("id", None)

                        if set_id:
                            set_item = WorkoutSet.objects.get(
                                id=set_id, workout_exercise=workout_exercise
                            )
                            set_item.set_number = set_data.get(
                                "set_number", set_item.set_number
                            )
                            set_item.reps = set_data.get("reps", set_item.reps)
                            set_item.weight = set_data.get("weight", set_item.weight)
                            set_item.save()
                        else:
                            WorkoutSet.objects.create(
                                workout_exercise=workout_exercise, **set_data
                            )

        return instance
