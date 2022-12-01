from rest_framework import viewsets, permissions, status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import (
    LoginSerializer, RegistrationSerializer, UserSerializer,
)
from .renderers import UserJSONRenderer
from django.http import HttpRequest, HttpResponse
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet, ViewSet

from .serializers import RegistrationSerializer
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework.permissions import AllowAny
from user.serializers import UserSerializer
from user.utils import generate_access_token, generate_refresh_token
from .models import User


class UserView(ModelViewSet):
    permission_classes = (AllowAny,)

    @action(detail=False)
    def profile(self, request: HttpRequest) -> HttpResponse:
        user = request.user
        serialized_user = UserSerializer(user).data
        return Response({'user': serialized_user})


class AuthAPIView(ModelViewSet):
    permission_classes = (AllowAny,)

    @action(detail=False, methods=['post'])
    def register(self, request: HttpRequest) -> HttpResponse:
        user = request.data.get('user', {})

        serializer = RegistrationSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def login(self, request: HttpRequest) -> HttpResponse:
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


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer_data = request.data.get('user', {})
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
