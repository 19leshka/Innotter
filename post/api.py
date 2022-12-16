from django.http import HttpRequest, HttpResponse
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from innotter.enum import MessageType
from innotter.producer import producer
from post.models import Post
from post.permissions import IsPostOwner
from post.serializers import PostSerializer, CreatePostSerializer, UpdatePostSerializer
from post.services import PostServices
from post.tasks import send_email
from user.permissioms import IsAdminOrModerator


class PostView(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated, )

    serializer_action_classes = {
        'create': CreatePostSerializer,
        'update': UpdatePostSerializer
    }

    permissions_mapping = {
        'destroy': IsPostOwner | IsAdminOrModerator,
    }

    def get_permissions(self):
        for actions, permission in self.permissions_mapping.items():
            if self.action in actions:
                self.permission_classes = (permission,)
        return super(self.__class__, self).get_permissions()

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()

    def list(self, request, *args, **kwargs):
        page = self.request.query_params.get('page')
        serializer = self.get_serializer_class()
        if page:
            queryset = self.queryset.filter(page=page)
        else:
            queryset = self.queryset
        serializer = serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        data = {**request.data, 'owner': self.request.user.id}
        serializer = self.get_serializer_class()
        serializer = serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        send_email.delay(serializer.data)
        producer({**serializer.data, 'type': MessageType.ADD_POST.value})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_destroy(self, instance):
        producer({'id': instance.page.id, 'type': MessageType.DEL_POST.value})
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        data = {**request.data, 'owner': self.request.user.id}
        serializer = self.get_serializer_class()
        serializer = serializer(instance=self.get_object(), data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['GET'], url_path='like', permission_classes=[IsAuthenticated], detail=True)
    def like(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        msg = PostServices.like_unlike_switch(self.get_object(), request)
        return Response(data=msg, status=status.HTTP_201_CREATED)

    @action(permission_classes=[IsAuthenticated], url_path='all-liked-posts', detail=False)
    def all_liked_posts(self, request: HttpRequest) -> HttpResponse:
        posts = request.user.liked_by_post.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(permission_classes=[IsAuthenticated], url_path='page-liked-posts', detail=True)
    def page_liked_posts(self, request: HttpRequest, pk: int) -> HttpResponse:
        posts = request.user.liked_by_post.filter(page=pk)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)