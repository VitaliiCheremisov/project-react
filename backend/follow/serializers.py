from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework import serializers
from rest_framework.serializers import ValidationError

from recipes.models import Recipe
from users.serializers import CustomUserSerializer, CustomUserShortSerializer
from .models import Follow

CustomUser = get_user_model()


class RecipeFollowSerializer(serializers.ModelSerializer):
    """Сериалайзер для подписок, необходим для правильной структуры ответа."""

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')


class FollowSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели подписок."""
    author = CustomUserSerializer(read_only=True)
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = ('id', 'author', 'is_subscribed', 'recipes', 'recipes_count')

    def get_is_subscribed(self, obj):
        """Проверка существования подписки."""
        return Follow.objects.filter(
            user=obj.user,
            author=obj.author
        ).exists()

    def get_recipes(self, obj):
        """Получение рецептов автора."""
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        queryset = Recipe.objects.filter(author=obj.author)
        if limit:
            queryset = queryset[:int(limit)]
        return RecipeFollowSerializer(queryset, many=True).data

    def get_recipes_count(self, obj):
        """Получение количества рецептов"""
        return Recipe.objects.filter(
            author=obj.author
        ).count()

    def to_representation(self, instance):
        """Изменение структуры ответа."""
        representation = CustomUserShortSerializer(instance.author).data
        representation['is_subscribed'] = self.get_is_subscribed(instance)
        representation['recipes'] = self.get_recipes(instance)
        representation['recipes_count'] = self.get_recipes_count(instance)
        return representation

    def validate(self, data):
        """Валидация данных."""
        user = self.context['request'].user
        author_id = self.context['view'].kwargs['id']
        author = get_object_or_404(CustomUser, id=author_id)
        if user == author:
            raise ValidationError('Нельзя подписаться на самого себя.')
        if Follow.objects.filter(user=user, author=author).exists():
            raise ValidationError('Подписка существует.')
        return data
