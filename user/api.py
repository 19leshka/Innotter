from django.http import HttpRequest, HttpResponse
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet, ViewSet
from .serializers import RegistrationSerializer
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework.permissions import AllowAny, IsAuthenticated
from user.serializers import UserSerializer
from user.utils import generate_access_token, generate_refresh_token
from user.models import User


class UserView(ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    @action(detail=False)
    def profile(self, request: HttpRequest) -> HttpResponse:
        user = request.user
        serialized_user = self.serializer_class(user).data
        return Response(serialized_user)

    @action(detail=False, url_path='update-profile', methods=['patch'])
    def update_profile(self, request: HttpRequest) -> HttpResponse:
        serializer_data = request.data
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class AuthAPIView(ViewSet):
    permission_classes = (AllowAny,)
    serializer_action_classes = {
        'register': RegistrationSerializer,
        'login': UserSerializer
    }

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()

    @action(detail=False, methods=['post'])
    def register(self, request: HttpRequest) -> HttpResponse:
        user = request.data.get('user', {})
        serializer = self.get_serializer_class()
        serializer = serializer(data=user)
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

        serializer = self.get_serializer_class()
        serialized_user = serializer(user).data

        access_token = generate_access_token(user)
        refresh_token = generate_refresh_token(user)

        response.set_cookie(key='refreshtoken', value=refresh_token, httponly=True)
        response.data = {
            'access_token': access_token,
            'user': serialized_user,
        }

        return response
