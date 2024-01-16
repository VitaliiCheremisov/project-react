from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.db.transaction import atomic

from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.serializers import ValidationError

from recipes.models import Ingredient
from tags.serializers import TagSerializer
from users.serializers import CustomUserSerializer
from .models import IngredientRecipes, Recipe, Tag
from .validators import ingredients_validator, tags_validator

CustomUser = get_user_model()


class IngredientSerializer(serializers.ModelSerializer):
    """Сериалайзер для ингредиентов."""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientRecipeSerializer(serializers.ModelSerializer):
    """Сериалайзер для связанной модели."""
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all()
    )
    name = serializers.CharField(
        source='ingredients.name',
        read_only=True
    )
    measurement_unit = serializers.CharField(
        source='ingredients.measurement_unit',
        read_only=True
    )

    class Meta:
        model = IngredientRecipes
        fields = ('id', 'name', 'measurement_unit', 'amount')


class AddIngredientSerializer(serializers.ModelSerializer):
    """Сериайлайзер для поля ingredient, создание рецепта."""
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all()
    )
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientRecipes
        fields = ('id', 'amount')


class RecipeShowSerializer(serializers.ModelSerializer):
    """Сериалайзер для отображения рецептов."""
    author = CustomUserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    ingredients = IngredientRecipeSerializer(
        many=True,
        source='recipe_ingredients',
        read_only=True
    )
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart',
                  'name', 'image', 'text', 'cooking_time')

    def get_is_favorited(self, obj):
        """Проверка избранного."""
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.favorite.filter(recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        """Проверка в списке покупок."""
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.shopping_cart.filter(recipe=obj).exists()


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Сериалайзер для создания рецептов."""
    ingredients = AddIngredientSerializer(
        many=True,
        write_only=True,
        required=True
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        required=True
    )
    image = Base64ImageField(required=True)
    author = CustomUserSerializer(read_only=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'ingredients', 'tags', 'image', 'name',
                  'text', 'cooking_time', 'author',
                  'is_favorited', 'is_in_shopping_cart')

    def get_is_favorited(self, obj):
        """Проверка избранного."""
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.favorite.filter(recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        """Проверка в списке покупок."""
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.shopping_cart.filter(recipe=obj).exists()

    def validate_image(self, value):
        """Валидация картинок."""
        if not isinstance(value, ContentFile):
            raise ValidationError('Неверный тип данных')
        return value

    def validate_tags(self, value):
        """Валидация тэгов."""
        tags = tags_validator(value, Tag)
        return tags

    def validate_ingredients(self, value):
        """Валидации данных для создания рецепта."""
        ingredients = ingredients_validator(value, Ingredient)
        return ingredients

    def validate(self, data):
        """Проверка наличия обязательных полей."""
        if 'tags' not in data:
            raise ValidationError('Нет тэгов')
        if 'ingredients' not in data:
            raise ValidationError('Нет ингредиентов.')
        return data

    def to_representation(self, instance):
        """Настройка структуры ответа."""
        representation = super().to_representation(instance)
        representation['tags'] = TagSerializer(instance.tags.all(),
                                               many=True).data
        representation['ingredients'] = IngredientRecipeSerializer(
            instance.recipe_ingredients.all(), many=True).data
        return representation

    def create_ingredients(self, ingredients, recipes):
        """Добавление ингредиентов."""
        IngredientRecipes.objects.bulk_create([
            IngredientRecipes(
                recipes=recipes,
                ingredients=ingredient['id'],
                amount=ingredient['amount'],
            ) for ingredient in ingredients
        ])

    @atomic
    def create(self, validated_data):
        """Создание рецепта"""
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = super().create(validated_data=validated_data)
        recipe.tags.set(tags)
        self.create_ingredients(ingredients, recipe)
        return recipe

    @atomic
    def update(self, instance, validated_data):
        """Обновление рецепта"""
        tags_data = validated_data.pop('tags')
        ingredients_data = validated_data.pop('ingredients')
        instance = super().update(instance, validated_data)
        tags = self.validate_tags(tags_data)
        ingredients = self.validate_ingredients(ingredients_data)
        instance.tags.set(tags)
        instance.ingredients.clear()
        self.create_ingredients(ingredients, instance)
        return instance


class RecipeShortSerializer(serializers.ModelSerializer):
    """Сериалайзер для отображения списка покупок и избранного."""
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'cooking_time', 'image')
