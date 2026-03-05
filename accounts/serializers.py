# accounts/serializers.py

from rest_framework import serializers
from django.contrib.auth.models import User


# Serializer for the registration of users


class RegisterSerializer(serializers.ModelSerializer):
    # write_only=True ensures that password hash won't be shown when json is returned to the user
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "password",
        )

    def create(self, validated_data):
        # create_user method saves password hash in the database
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
            email=validated_data.get("email", ""),
        )
        return user
