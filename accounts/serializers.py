# accounts/serializers.py

from rest_framework import serializers
from django.contrib.auth.models import User



# Serializer for the registration of users

class RegisterSerializer(serializers.ModelSerializer):
    # write_only=True ensures that password won't be shown in response
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "password",
        )

    def create(self, validated_data):
        # hashing of passwords
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
        )
        return user
