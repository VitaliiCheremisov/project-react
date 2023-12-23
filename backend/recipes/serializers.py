from django.db.transaction import atomic
from drf_extra_fields.fields import Base64ImageField
from recipes.models import Ingredient
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from tags.serializers import TagSerializer
from users.serializers import CustomUserSerializer

from .models import Follow, IngredientRecipes, Recipe, Tag
from .validators import ingredients_validator, tags_validator


class IngredientSerializer(serializers.ModelSerializer):
    """Сериалайзер для ингредиентов."""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')
        read_only_fields = ('id', 'name', 'measurement_unit')


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


class RecipeSerializer(serializers.ModelSerializer):
    """Сериалайзер для создания рецептов."""
    ingredients = IngredientRecipeSerializer(
        many=True, source='recipe_ingredients', read_only=True
    )
    tags = TagSerializer(many=True)
    image = Base64ImageField()
    author = CustomUserSerializer(read_only=True)
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

    def validate(self, data):
        """Валидации данных для создания рецепта."""
        tags_data = self.initial_data.get('tags')
        ingredients_data = self.initial_data.get('ingredients')
        tags = tags_validator(tags_data, Tag)
        ingredients = ingredients_validator(
            ingredients_data, Ingredient
        )
        if not data.get('image'):
            raise ValidationError('Пустое поле image')
        if not data.get('text'):
            raise ValidationError('Пустое поле text')
        if not data.get('cooking_time'):
            raise ValidationError('Пустое поле cooking_time')
        data['tags'] = tags
        data['ingredients'] = ingredients
        return data

    def create_ingredients(self, ingredients, recipes):
        """Добавление ингредиентов."""
        IngredientRecipes.objects.bulk_create([
            IngredientRecipes(
                recipes=recipes,
                ingredients=ingredient['ingredients'],
                amount=ingredient['amount'],
            ) for ingredient in ingredients
        ])

    @atomic
    def create(self, validated_data):
        """Создание рецепта"""
        image = validated_data.pop('image')
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(image=image, **validated_data)
        recipe.tags.set(tags)
        self.create_ingredients(ingredients, recipe)
        return recipe

    @atomic
    def update(self, instance, validated_data):
        """Обновление рецепта"""
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )
        instance.tags.clear()
        tags_data = self.initial_data.get('tags')
        instance.tags.set(tags_data)
        IngredientRecipes.objects.filter(recipes=instance).all().delete()
        self.create_ingredients(validated_data.get('ingredients'), instance)
        instance.save()
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
