from rest_framework import serializers

from innotter.enum import MessageType
from innotter.producer import producer
from post.models import Post
from tag.serializers import TagSerializer
from user.serializers import UserSerializer
from .models import Page


class BlockPageSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if not ret['is_blocked']:
            return ret


class PageSerializer(BlockPageSerializer, serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    owner = UserSerializer(read_only=True)
    followers = UserSerializer(read_only=True, many=True)

    class Meta:
        model = Page
        fields = (
            'id', 'uuid', 'name', 'tags', 'image', 'description', 'owner', 'followers', 'is_private', 'is_blocked', 'image')
        read_only_fields = ('followers',)


class CreatePageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ('id', 'uuid', 'name', 'tags', 'image', 'owner', 'description', 'image', 'is_private')


class UpdatePageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ('id', 'uuid', 'name', 'tags', 'image', 'owner', 'description', 'is_private', 'image')


class PageOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ('id', 'uuid', 'name', 'tags', 'owner', 'description', 'followers', 'follow_requests', 'is_private', 'image', 'is_blocked', 'unblock_date')
        read_only_fields = ('is_blocked', 'unblock_date')


class ApproveRequestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ('follow_requests', 'followers')

    def update(self, page, validated_data):
        users = validated_data.pop('follow_requests')
        for user in users:
            page.follow_requests.remove(user)
            page.followers.add(user)
        page.save()
        producer({'id': page.id, 'count': len(users), 'value': 'total_followers', 'type': MessageType.ADD_LIKE.value})
        return page


class RejectRequestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ('follow_requests', 'followers')

    def update(self, page, validated_data):
        users = validated_data.pop('follow_requests')
        for user in users:
            page.follow_requests.remove(user)

        page.save()
        return page
