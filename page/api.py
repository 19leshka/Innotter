from django.http import HttpRequest, HttpResponse
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from page.permissions import PageAccessPermission
from page.services import PageService
from tag.services import TagService
from page.models import Page
from page.serializers import PageSerializer, CreatePageSerializer, UpdatePageSerializer


class PagesView(ModelViewSet):
    queryset = Page.objects.all()
    permission_classes = (IsAuthenticated, PageAccessPermission)
    serializer_class = PageSerializer

    serializer_action_classes = {
        'create': CreatePageSerializer,
        'update': UpdatePageSerializer,
    }

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        tags_id = TagService.process_tags(request)
        data = {**request.data, 'tags': tags_id, 'owner': self.request.user.id}
        serializer = self.get_serializer_class()
        serializer = serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        tags_id = TagService.process_tags(request)
        data = {**request.data, 'tags': tags_id, 'owner': self.request.user.id}
        serializer = self.get_serializer_class()
        serializer = serializer(instance=self.get_object(), data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(url_path='follow', permission_classes=[IsAuthenticated], detail=True)
    def follow(self, request: HttpRequest, pk=None) -> HttpResponse:
        message = PageService.follow_unfollow_switch(pk, request)
        return Response(data=message, status=status.HTTP_201_CREATED)