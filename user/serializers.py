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
        if 'image' in validated_data:
            if validated_data.image.rsplit('.')[-1].lower() not in ALLOWED_IMAGE_EXTENSIONS:
                raise serializers.ValidationError(
                    {'status': f'Invalid uploaded image type: {validated_data.image}'}
                )

            image = AwsService.upload_file(validated_data.image, 'user' + str(User.objects.latest('id').id + 1))

            validated_data.image = image

        return User.objects.create_user(**validated_data)
