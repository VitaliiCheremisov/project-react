from django.shortcuts import get_object_or_404

from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ValidationError

from recipes.models import Recipe
from .models import ShoppingCart
from .serializers import ShoppingCartDisplaySerializer, ShoppingCartSerializer


class ShoppingCartViewSet(mixins.CreateModelMixin,
                          mixins.DestroyModelMixin,
                          viewsets.GenericViewSet):
    """Работа со списком покупок."""
    serializer_class = ShoppingCartSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'

    def get_serializer_class(self):
        """Выбор сериалайзера."""
        if self.request.method == 'GET':
            return ShoppingCartDisplaySerializer
        return ShoppingCartSerializer

    def get_serializer(self, *args, **kwargs):
        """Изменение данных из запроса."""
        kwargs['data'] = {'user': self.request.user.id,
                          'recipe': self.kwargs['id']}
        return super().get_serializer(*args, **kwargs)

    def get_object(self):
        """Получение объекта для удаления."""
        recipe = get_object_or_404(Recipe, id=self.kwargs['id'])
        queryset = ShoppingCart.objects.filter(
            user=self.request.user,
            recipe__id=recipe.id
        )
        if not queryset:
            raise ValidationError('Рецепта не существует.')
        return queryset.first()
