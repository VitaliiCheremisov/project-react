from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.serializers import ValidationError
from rest_framework.validators import UniqueTogetherValidator

from recipes.models import Recipe
from recipes.serializers import RecipeShortSerializer
from .models import ShoppingCart

CustomUser = get_user_model()


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Сериайлайзер для списка покупок."""
    user = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all()
    )
    recipe = serializers.PrimaryKeyRelatedField(
        queryset=Recipe.objects.all()
    )

    class Meta:
        model = ShoppingCart
        fields = ('user', 'recipe')
        validators = [
            UniqueTogetherValidator(
                queryset=ShoppingCart.objects.all(),
                fields=('user', 'recipe')
            )
        ]

    def to_representation(self, instance):
        """Изменение структуры ответа."""
        representation = RecipeShortSerializer(instance.recipe).data
        return representation

    def validate(self, data):
        """Проверка данных."""
        user = self.context['request'].user
        recipe_id = self.context['view'].kwargs['id']
        recipe = Recipe.objects.get(id=recipe_id)
        if not recipe:
            raise ValidationError('Рецепта не существует.')
        if ShoppingCart.objects.filter(user=user, recipe=recipe).exists():
            raise ValidationError('Рецепт уже в списке покупок.')
        return data


class ShoppingCartDisplaySerializer(serializers.ModelSerializer):
    """Серилайзер для отображения списка покупок."""
    recipe = RecipeShortSerializer()

    class Meta:
        model = ShoppingCart
        fields = ('user', 'recipe')

    def to_representation(self, instance):
        """Изменение структуры ответа."""
        representation = RecipeShortSerializer(instance.recipe).data
        return representation
