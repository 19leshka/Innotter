from django.http import HttpRequest, HttpResponse
from rest_framework import status
from rest_framework.viewsets import ModelViewSet

from .serializers import RegistrationSerializer
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework.permissions import AllowAny
from user.serializers import UserSerializer
from user.utils import generate_access_token, generate_refresh_token

class RegistrationAPIView(ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    def create(self, request: HttpRequest) -> HttpResponse:
        user = request.data.get('user', {})

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserView(ModelViewSet):
    permission_classes = (AllowAny,)
    def list(self, request: HttpRequest) -> HttpResponse:
        user = request.user
        serialized_user = UserSerializer(user).data
        return Response({'user': serialized_user})


class LoginAPIView(ModelViewSet):
    permission_classes = (AllowAny,)

    def create(self, request: HttpRequest) -> HttpResponse:
        User = get_user_model()
        email = request.data.get('email')
        password = request.data.get('password')
        response = Response()
        if (email is None) or (password is None):
            raise exceptions.AuthenticationFailed(
                'email or password required')

        user = User.objects.filter(email=email).first()
        if user is None:
            raise exceptions.AuthenticationFailed('user not found')
        if not user.check_password(password):
            raise exceptions.AuthenticationFailed('wrong password')

        serialized_user = UserSerializer(user).data

        access_token = generate_access_token(user)
        refresh_token = generate_refresh_token(user)

        response.set_cookie(key='refreshtoken', value=refresh_token, httponly=True)
        response.data = {
            'access_token': access_token,
            'user': serialized_user,
        }

        return response
