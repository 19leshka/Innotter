from django.http import HttpRequest, HttpResponse
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from page.permissions import PageAccessPermission, IsPageOwner
from page.services import PageService
from post.serializers import PostSerializer
from tag.services import TagService
from page.models import Page
from page.serializers import PageSerializer, CreatePageSerializer, UpdatePageSerializer, ApproveRequestsSerializer, \
    PageOwnerSerializer, RejectRequestsSerializer
from user.models import User
from user.serializers import UserSerializer


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

    def create(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        tags_id = TagService.process_tags(request)
        data = {**request.data, 'tags': tags_id, 'owner': self.request.user.id}
        serializer = self.get_serializer_class()
        serializer = serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        tags_id = TagService.process_tags(request)
        data = {**request.data, 'tags': tags_id, 'owner': self.request.user.id}
        serializer = self.get_serializer_class()
        serializer = serializer(instance=self.get_object(), data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

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
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(permission_classes=[IsAuthenticated], url_path='all-liked-posts', detail=False)
    def all_liked_posts(self, request: HttpRequest) -> HttpResponse:
        posts = User.objects.get(pk=request.user.id).liked_by_post.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(permission_classes=[IsAuthenticated], url_path='page-liked-posts', detail=True)
    def page_liked_posts(self, request: HttpRequest, pk: int) -> HttpResponse:
        posts = User.objects.get(pk=request.user.id).liked_by_post.filter(page=pk)
        serializer = PostSerializer(posts, many=True)
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
