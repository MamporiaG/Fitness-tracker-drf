# accounts/views.py

from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RegisterSerializer, LoginSerializer
from drf_spectacular.utils import extend_schema


class RegisterView(APIView):
    """
    Default permissions (requirement to authenticate for request submission) is overriden.
    Data validity is checked. In case data validation fails, HTTP 400 response bill be raised.
    """

    permission_classes = [AllowAny]

    @extend_schema(request=RegisterSerializer)
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    Default permissions (requirement to authenticate for request submission) is overriden.
    Built-in authenticate() function checks usersname and password hash and returns either User object or None.
    """

    permission_classes = [AllowAny]

    @extend_schema(request=LoginSerializer)
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return Response({"detail": f"Welcome, {user.username}!"})
        else:
            return Response(
                {"detail": "Invalid username or password."},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class LogoutView(APIView):
    """
    Built-in logout() function deletes session from the db and sessionid from the browser cookies
    """

    def post(self, request):
        logout(request)
        return Response({"detail": "Logged out successfully."})
