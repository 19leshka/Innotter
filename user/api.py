from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status, serializers
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet, ViewSet

from innotter.services import AwsService
from .permissioms import IsAdmin
from .serializers import RegistrationSerializer
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework.permissions import AllowAny, IsAuthenticated
from user.serializers import UserSerializer
from user.utils import generate_access_token, generate_refresh_token
from user.models import User
from .services import UserService


class UserView(ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        serializer = UserSerializer(self.queryset, many=True)
        for user in serializer.data:
            user['image'] = AwsService.get_file_url(user['image'])
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk):
        user = get_object_or_404(self.queryset, pk=pk)
        serialized_data = UserSerializer(user).data
        image = AwsService.get_file_url(key=serialized_data['image'])
        serialized_data['image'] = image
        return Response(serialized_data, status=status.HTTP_200_OK)

    @action(detail=False)
    def profile(self, request: HttpRequest) -> HttpResponse:
        serialized_user_data = self.serializer_class(request.user).data
        serialized_user_data['image'] = AwsService.get_file_url(serialized_user_data['image'])
        return Response(serialized_user_data, status=status.HTTP_200_OK)

    @action(detail=False, url_path='update-profile', methods=['patch'])
    def update_profile(self, request: HttpRequest) -> HttpResponse:
        serializer_data = request.data

        if 'image' in request.data:
            image = AwsService.upload_file(request.data['image'], str(request.user.image))
            serializer_data['image'] = image

        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'], permission_classes=[IsAdmin])
    def block(self, request: HttpRequest, pk: int) -> HttpResponse:
        data = UserService.block_unblock_switch(pk)
        return Response(data, status=status.HTTP_200_OK)


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
        data = request.data

        if 'image' in request.data:
            image = AwsService.upload_file(request.data['image'], 'user' + str(User.objects.latest('id').id + 1))
            data['image'] = image

        serializer = self.get_serializer_class()
        serializer = serializer(data=data)
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
