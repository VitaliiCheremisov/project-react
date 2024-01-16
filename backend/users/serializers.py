from django.contrib.auth import get_user_model

from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from rest_framework.serializers import ValidationError

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
        return (not self.context.get('request').user.is_anonymous
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

    def validate_username(self, value):
        """Проверка на создание me."""
        disallowed_usernames = ['me']
        if value.lower() in disallowed_usernames:
            raise ValidationError('Имя пользователя "me" запрещено.')
        return value


class CustomUserShortSerializer(UserSerializer):
    """Сериалайзер для отображения в follow."""

    class Meta:
        model = CustomUser
        fields = ('username',
                  'first_name',
                  'last_name',
                  'email',
                  'id',)
