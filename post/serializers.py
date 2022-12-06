from page import serializers
from page.serializers import PageSerializer
from post.models import Post


class PostSerializer(serializers.ModelSerializer):
    page = PageSerializer()

    class Meta:
        model = Post
        fields = ('id', 'page', 'created_at', 'updated_at', 'reply_to', 'liked_by')


class CreatePostSerializer(serializers.ModelSerializer):
    page = PageSerializer

    class Meta:
        model = Post
        fields = ('id', 'page', 'content', 'owner', 'reply_to')


class UpdatePostSerializer(serializers.ModelSerializer):
    page = PageSerializer()

    class Meta:
        model = Post
        fields = ('id', 'page', 'content', 'owner', 'reply_to')
