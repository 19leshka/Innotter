from django.http import HttpRequest, HttpResponse
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from tag.services import TagService
from user.serializers import UserSerializer
from .models import Page
from .serializers import PageSerializer, PageSerializer, CreatePageSerializer


class PagesView(ModelViewSet):
    queryset = Page.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = PageSerializer

    def list(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        serializer = PageSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        tags_id = TagService.process_tags(request)
        data = {**request.data, 'tags': tags_id, 'owner': self.request.user.id}
        serializer = CreatePageSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)