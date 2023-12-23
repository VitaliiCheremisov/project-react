from api.permissions import IsAuthorOrReadOnly
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from users.models import CustomUser

from .filters import IngredientSearchFilter, RecipeFilter
from .models import Follow, Ingredient, Recipe
from .paginators import CustomPaginator
from .serializers import (FollowSerializer, IngredientSerializer,
                          RecipeSerializer)
from .utils import calculate_shopping_cart


class IngredientViewSet(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    """Работа с ингредиентами."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    filter_backends = (IngredientSearchFilter,)
    search_fields = ('^name',)

    def create(self, request, *arg, **kwargs):
        """Обрабатываем запрос на создание ингредиента."""
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def list(self, request, *args, **kwargs):
        """Убираем дополнительную информацию в ответе api."""
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class RecipeViewSet(viewsets.ModelViewSet):
    """Работа с рецептами."""

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = CustomPaginator
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        """Созднание рецепта."""
        serializer.save(author=self.request.user)

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
        if author.shopping_cart.exists():
            return calculate_shopping_cart(self, request, author)
        return Response(status=status.HTTP_404_NOT_FOUND)


class FollowViewSet(viewsets.ModelViewSet):
    """Работа с подписками пользователя."""

    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        """Создание подписки."""
        user = get_object_or_404(CustomUser, id=self.kwargs['id'])
        if self.request.user == user:
            raise ValidationError('Нельзя подписаться на самого себя')
        if Follow.objects.filter(user=self.request.user, author=user).exists():
            raise ValidationError('Подписка уже существует.')
        serializer.save(user=self.request.user, author=user)

    def delete(self, request, *args, **kwargs):
        """Удаление подписки"""
        author = get_object_or_404(CustomUser, id=self.kwargs['id'])
        if not Follow.objects.filter(user=request.user,
                                     author=author).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        Follow.objects.filter(user=request.user, author=author).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
