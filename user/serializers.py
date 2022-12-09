from rest_framework import serializers

from innotter.services import AwsService
from user.models import User


ALLOWED_IMAGE_EXTENSIONS = ('png', 'jpg', 'jpeg')


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'is_active', 'image']

    def update(self, instance, validated_data):
        password = validated_data.get('password')

        for key, value in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        instance.save()

        return instance


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'image']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
