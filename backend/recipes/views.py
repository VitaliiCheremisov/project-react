from django.db.models import Sum
from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS, AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

from foodgram.permissions import IsAuthorOrReadOnly
from users.models import CustomUser

from .filters import IngredientSearchFilter, RecipeFilter
from .models import Follow, Ingredient, IngredientRecipes, Recipe
from .serializers import (FollowSerializer, IngredientSerializer,
                          RecipeCreateSerializer, RecipeShowSerializer)
from .utils import calculate_shopping_cart


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Работа с ингредиентами."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    filter_backends = (IngredientSearchFilter,)
    search_fields = ('^name',)

    def get_paginated_response(self, data):
        """Изменение структуры ответа."""
        return Response(data)


class RecipeViewSet(viewsets.ModelViewSet):
    """Работа с рецептами."""

    queryset = Recipe.objects.all()
    permission_classes = (IsAuthorOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        """Создание рецепта."""
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        """Выбор сериалайзера в зависимости от метода."""
        if self.request.method in SAFE_METHODS:
            return RecipeShowSerializer
        return RecipeCreateSerializer

    @action(
        detail=False,
        methods=['get'],
        url_path='download_shopping_cart',
        url_name='download_shopping_cart',
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request, **kwargs):
        """Скачивание списка покупок."""
        author = CustomUser.objects.get(id=self.request.user.id)
        ingredients_in_recipes = IngredientRecipes.objects.filter(
            recipes__shopping_cart__user=author
        ).values(
            'ingredients__name', 'ingredients__measurement_unit'
        ).annotate(amounts=Sum('amount', distinct=True)).order_by('amounts')
        if author.shopping_cart.exists():
            shopping_cart = calculate_shopping_cart(ingredients_in_recipes)
            response = Response(shopping_cart, content_type='text/plain')
            response['Content-Disposition'] = ('attachment; '
                                               'filename="shopping_list.txt"')
            return response
        return Response(status=status.HTTP_404_NOT_FOUND)


class FollowViewSet(viewsets.ModelViewSet):
    """Работа с подписками пользователя."""

    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'

    def perform_create(self, serializer):
        """Создание подписки."""
        serializer.save(user=self.request.user,
                        author=get_object_or_404(
                            CustomUser,
                            id=self.kwargs['id'])
                        )

    def get_queryset(self):
        """Получение кверисета для удаления."""
        queryset = super().get_queryset()
        author = get_object_or_404(CustomUser, id=self.kwargs['id'])
        filtered_queryset = queryset.filter(user=self.request.user,
                                            author=author)
        return filtered_queryset

    def get_object(self):
        """Получение объекта для удаления"""
        queryset = self.get_queryset()
        if not queryset:
            raise ValidationError('Подписки не существует')
        return queryset.first()
