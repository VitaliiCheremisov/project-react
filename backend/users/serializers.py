from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from rest_framework.serializers import ValidationError

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

    def validate(self, data):
        """Валидация данных."""
        if 'first_name' not in data:
            raise ValidationError('Поле "first_name обязательно."')
        if 'last_name' not in data:
            raise ValidationError('Поле "last_name" обязательно.')
        return data
