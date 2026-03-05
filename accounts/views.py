from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RegisterSerializer


class RegisterView(APIView):
    # AllowAny overrides the global IsAuthenticated setting — anyone can register
    permission_classes = [AllowAny]

    def post(self, request):
        # conducts validation checks
        serializer = RegisterSerializer(data=request.data)
        if (
            serializer.is_valid()
        ):  # if the username is unique and if the password is 6+ characters
            serializer.save()  # .save method calls create() method
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        # authenticate() checks the username and password in the database
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # login() creates a session — future requests from this client are recognized
            login(request, user)
            return Response({"detail": f"Welcome, {user.username}!"})
        else:
            return Response(
                {"detail": "Invalid username or password."},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({"detail": "Logged out successfully."})
