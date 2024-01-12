from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.serializers import ValidationError
from rest_framework.validators import UniqueTogetherValidator

from recipes.models import Recipe

from .models import Favorite

CustomUser = get_user_model()


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериалайзер для избранного."""
    user = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all()
    )
    recipe = serializers.PrimaryKeyRelatedField(
        queryset=Recipe.objects.all()
    )
    image = serializers.SerializerMethodField()

    class Meta:
        model = Favorite
        fields = ('user', 'recipe', 'image')
        validators = [
            UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=('user', 'recipe')
            )
        ]

    def get_image(self, obj):
        """Обработка поля image для передачи в ответ."""
        return obj.recipe.image.url

    def to_representation(self, instance):
        """Изменение структуры ответа."""
        representation = super().to_representation(instance)
        representation['id'] = instance.recipe.id
        representation['name'] = instance.recipe.name
        representation['cooking_time'] = instance.recipe.cooking_time
        del representation['recipe']
        del representation['user']
        return representation

    def validate(self, data):
        """Проверка данных."""
        user = self.context['request'].user
        recipe_id = self.context['view'].kwargs['id']
        recipe = Recipe.objects.get(id=recipe_id)
        if not recipe:
            raise ValidationError('Рецепта не существует.')
        if Favorite.objects.filter(user=user, recipe=recipe).exists():
            raise ValidationError('Рецепт уже в избранном')
        return data
