from django.contrib.auth import get_user_model

from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from follow.models import Follow

CustomUser = get_user_model()


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
        return (not user.is_anonymous
                and Follow.objects.
                filter(user=self.context.get('request').user,
                       author=obj.id).exists())


class CustomUserCreateSerializer(UserCreateSerializer):
    """Сериалайзер для создания пользователя."""

    class Meta:
        model = CustomUser
        fields = ('email',
                  'id',
                  'password',
                  'username',
                  'first_name',
                  'last_name')
