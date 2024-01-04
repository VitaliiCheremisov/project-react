from django.db.transaction import atomic
from django.shortcuts import get_object_or_404

from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.serializers import ValidationError

from recipes.models import Ingredient
from tags.serializers import TagSerializer
from users.models import CustomUser
from users.serializers import CustomUserSerializer

from .models import Follow, IngredientRecipes, Recipe, Tag
from .validators import ingredients_validator, tags_validator


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
        fields = ['id', 'name', 'measurement_unit', 'amount']


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
        write_only=True
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    image = Base64ImageField()
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
        """Проверка наличия поля "image"."""
        if not value:
            raise ValidationError('Пустое поле image.')
        return value

    def validate_tags(self, value):
        """Валидация тэгов."""
        tags = tags_validator(value, Tag)
        return tags

    def validate_ingredients(self, value):
        """Валидации данных для создания рецепта."""
        ingredients = ingredients_validator(value, Ingredient)
        return ingredients

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
        try:
            tags_data = validated_data.pop('tags')
        except KeyError:
            raise ValidationError('Нет тэгов.')
        try:
            ingredients_data = validated_data.pop('ingredients')
        except KeyError:
            raise ValidationError('Нет ингредиентов.')
        instance = super().update(instance, validated_data)
        tags = self.validate_tags(tags_data)
        ingredients = self.validate_ingredients(ingredients_data)
        instance.tags.set(tags)
        instance.ingredients.clear()
        self.create_ingredients(ingredients, instance)
        return instance


class RecipeFollowSerializer(serializers.ModelSerializer):
    """Сериалайзер для подписок, необходим для правильной структуры ответа."""

    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')


class FollowSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели подписок."""
    id = serializers.ReadOnlyField(source='author.id')
    email = serializers.ReadOnlyField(source='author.email')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = ('id', 'email', 'username', 'first_name',
                  'last_name', 'is_subscribed', 'recipes',
                  'recipes_count')

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

    def validate(self, data):
        user = self.context['request'].user
        author_id = self.context['view'].kwargs['id']
        author = get_object_or_404(CustomUser, id=author_id)
        if user == author:
            raise ValidationError('Нельзя подписаться на самого себя.')
        if Follow.objects.filter(user=user, author=author).exists():
            raise ValidationError('Подписка существует.')
        return data
