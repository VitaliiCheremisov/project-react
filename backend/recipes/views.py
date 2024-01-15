from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import HttpResponse

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS, AllowAny, IsAuthenticated
from rest_framework.response import Response

from core.permissions import IsAuthorOrReadOnly
from .filters import IngredientSearchFilter, RecipeFilter
from .models import Ingredient, IngredientRecipes, Recipe
from .serializers import (IngredientSerializer, RecipeCreateSerializer,
                          RecipeShowSerializer)
from .utils import calculate_shopping_cart

CustomUser = get_user_model()


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Работа с ингредиентами."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    filter_backends = (IngredientSearchFilter,)
    search_fields = ('^name',)
    pagination_class = None


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
            response = HttpResponse(shopping_cart,
                                    content_type='text/plain; charset=utf-8')
            response['Content-Disposition'] = ('attachment; '
                                               'filename="shopping_list.txt"')
            return response
        return Response(status=status.HTTP_404_NOT_FOUND)
