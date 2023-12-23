from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

from recipes.models import Recipe
from recipes.paginators import CustomPaginator

from .models import ShoppingCart
from .serializers import ShoppingCartSerializer


class ShoppingCartViewSet(viewsets.ModelViewSet):
    """Работа со списком покупок."""
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPaginator

    def create(self, request, *args, **kwargs):
        """Добавление в список покупок."""
        recipe = Recipe.objects.filter(
            id=self.kwargs['id']
        ).first()
        if not recipe:
            raise ValidationError('Рецепта не существует.')
        if ShoppingCart.objects.filter(
                user=self.request.user,
                recipe=recipe
        ).exists():
            raise ValidationError('Рецепт уже в списке покупок.')
        ShoppingCart.objects.create(user=request.user, recipe=recipe)
        serializer = ShoppingCartSerializer()
        return Response(
            serializer.to_representation(instance=recipe),
            status=status.HTTP_201_CREATED,
        )

    def delete(self, request, *args, **kwargs):
        """Удаление рецепта из списка покупок"""
        recipe = Recipe.objects.filter(id=self.kwargs['id']).first()
        if not recipe:
            return Response(status=status.HTTP_404_NOT_FOUND)
        shopping_cart = ShoppingCart.objects.filter(
            user__id=request.user.id,
            recipe__id=self.kwargs['id']
        ).first()
        if shopping_cart is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        ShoppingCart.objects.filter(user__id=request.user.id,
                                    recipe__id=self.kwargs['id']).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
