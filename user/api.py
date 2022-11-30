from django.http import HttpRequest, HttpResponse
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .serializers import RegistrationSerializer, LoginSerializer
from .renderers import UserJSONRenderer


class RegistrationAPIView(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegistrationSerializer
    renderer_classes = (UserJSONRenderer,)

    def create(self, request: HttpRequest) -> HttpResponse:
        user = request.data.get('user', {})

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def create(self, request: HttpRequest) -> HttpResponse:
        user = request.data.get('user', {})

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
