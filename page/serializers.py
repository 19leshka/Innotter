from rest_framework import serializers

from tag.serializers import TagSerializer
from user.serializers import UserSerializer
from .models import Page


class PageSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    owner = UserSerializer(read_only=True)
    followers = UserSerializer(read_only=True, many=True)

    class Meta:
        model = Page
        fields = (
            'id', 'uuid', 'name', 'tags', 'image', 'description', 'owner', 'followers', 'is_private',)
        read_only_fields = ('followers',)


class CreatePageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ('id', 'uuid', 'name', 'tags', 'image', 'owner', 'description', 'is_private')


class UpdatePageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ('id', 'uuid', 'name', 'tags', 'image', 'owner', 'description', 'is_private')


class PageOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ('id', 'uuid', 'name', 'tags', 'owner', 'description', 'followers', 'follow_requests', 'is_private',
                  'is_blocked', 'unblock_date')
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
