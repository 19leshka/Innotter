from rest_framework import serializers

from page.models import Page
from page.serializers import PageSerializer
from post.models import Post
from user.serializers import UserSerializer


class PostSerializer(serializers.ModelSerializer):
    page = PageSerializer()

    class Meta:
        model = Post
        fields = ('id', 'page', 'owner', 'created_at', 'updated_at', 'reply_to', 'liked_by')
        read_only_fields = ('created_at', 'updated_at', 'reply_to')


class CreatePostSerializer(serializers.ModelSerializer):
    page = PageSerializer

    class Meta:
        model = Post
        fields = ('id', 'page', 'content', 'owner', 'reply_to')


class UpdatePostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('id', 'page', 'content', 'owner', 'reply_to')


