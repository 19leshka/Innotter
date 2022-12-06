from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from post.models import Post
from post.serializers import PostSerializer, CreatePostSerializer, UpdatePostSerializer


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated, )

    serializer_action_classes = {
        'create': CreatePostSerializer,
        'update': UpdatePostSerializer
    }

    def create(self, request, *args, **kwargs):
        data = {**request.data, 'owner': self.request.user.id}
        serializer = self.get_serializer_class()
        serializer = serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)