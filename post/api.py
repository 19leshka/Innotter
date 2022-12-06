from django.http import HttpRequest, HttpResponse
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from post.models import Post
from post.serializers import PostSerializer, CreatePostSerializer, UpdatePostSerializer
from post.services import PostServices


class PostView(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated, )

    serializer_action_classes = {
        'create': CreatePostSerializer,
        'update': UpdatePostSerializer
    }

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
        return Response(data, status=status.HTTP_201_CREATED)

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
