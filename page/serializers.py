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

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()

        return instance


class CreatePageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ('id', 'uuid', 'name', 'tags', 'image', 'owner', 'description', 'is_private')


class UpdatePageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ('id', 'uuid', 'name', 'tags', 'image', 'owner', 'description', 'is_private')

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance
