from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from innotter.producer import producer
from innotter.services import AwsService
from innotter.enum import MessageType
from page.permissions import PageAccessPermission, IsPageOwner
from page.services import PageService
from tag.services import TagService
from page.models import Page
from page.serializers import PageSerializer, CreatePageSerializer, UpdatePageSerializer, ApproveRequestsSerializer, \
    PageOwnerSerializer, RejectRequestsSerializer
from user.permissioms import IsAdminOrModerator


class PagesView(ModelViewSet):
    queryset = Page.objects.all()
    permission_classes = (IsAuthenticated, PageAccessPermission)
    serializer_class = PageSerializer

    serializer_action_classes = {
        'create': CreatePageSerializer,
        'update': UpdatePageSerializer,
        'my-pages': PageOwnerSerializer
    }

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()

    def list(self, request, *args, **kwargs):
        serializer = PageSerializer(self.queryset, many=True)
        for page in serializer.data:
            page['image'] = AwsService.get_file_url(page['image'])
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk):
        page = get_object_or_404(self.queryset, pk=pk)
        serialized_data = PageSerializer(page).data
        image = AwsService.get_file_url(key=serialized_data['image'])
        serialized_data['image'] = image
        return Response(serialized_data, status=status.HTTP_200_OK)

    def create(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        tags_id = TagService.process_tags(request)
        image = None
        if 'image' in request.data:
            image = AwsService.upload_file(self.request.data['image'], 'page' + str(Page.objects.latest('id').id + 1))
        data = {'name': request.data['name'], 'description': request.data['description'], 'tags': tags_id, 'owner': request.user.id, 'image': image}
        serializer = self.get_serializer_class()
        serializer = serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        producer({**serializer.data, 'type': MessageType.CREATE.value})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        tags_id = TagService.process_tags(request)
        data = {'name': request.data['name'], 'description': request.data['description'], 'tags': tags_id, 'owner': self.request.user.id}
        if 'image' in request.data:
            image = AwsService.upload_file(request.data['image'], str(request.user.image))
            data['image'] = image
        serializer = self.get_serializer_class()
        serializer = serializer(instance=self.get_object(), data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        producer({'id': instance.id, 'type': MessageType.DELETE.value})
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(url_path='follow', permission_classes=[IsAuthenticated], detail=True)
    def follow(self, request: HttpRequest, pk: int = None) -> HttpResponse:
        message = PageService.follow_unfollow_switch(pk, request)
        return Response(data=message, status=status.HTTP_201_CREATED)

    @action(permission_classes=[IsAuthenticated], url_path='my-pages', detail=False)
    def my_pages(self, request: HttpRequest) -> HttpResponse:
        user = request.user
        queryset = Page.objects.filter(owner=user)
        serializer = self.get_serializer_class()
        serializer = serializer(queryset, many=True)
        for page in serializer.data:
            page['image'] = AwsService.get_file_url(page['image'])
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['PATCH'], url_path='approve-requests', permission_classes=[IsPageOwner],
            detail=True)
    def approve_requests(self, request: HttpRequest, pk: int) -> HttpResponse:
        serializer = ApproveRequestsSerializer(self.get_object(), request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['PATCH'], url_path='reject-requests', permission_classes=[IsPageOwner],
            detail=True)
    def reject_requests(self, request: HttpRequest, pk: int) -> HttpResponse:
        serializer = RejectRequestsSerializer(self.get_object(), request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'], permission_classes=[IsAdminOrModerator])
    def block(self, request: HttpRequest, pk: int) -> HttpResponse:
        data = PageService.block_unblock(pk)
        return Response(data, status=status.HTTP_200_OK)
