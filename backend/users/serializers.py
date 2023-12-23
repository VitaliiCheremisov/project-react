from rest_framework import serializers

from djoser.serializers import UserCreateSerializer, UserSerializer

from recipes.models import Follow

from .models import CustomUser


class CustomUserSerializer(UserSerializer):
    """Сериалайзер для модели пользователя."""
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CustomUser
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        """Получаем подписки пользователя."""
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Follow.objects.filter(user=user, author=obj.id).exists()


class CustomUserCreateSerializer(UserCreateSerializer):
    """Сериалайзер для созлания пользователя."""

    class Meta:
        model = CustomUser
        fields = ('email',
                  'id',
                  'password',
                  'username',
                  'first_name',
                  'last_name')
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True},
            'password': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }
