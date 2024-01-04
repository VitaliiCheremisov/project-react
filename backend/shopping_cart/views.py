from django.shortcuts import get_object_or_404

from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ValidationError

from recipes.models import Recipe

from .models import ShoppingCart
from .serializers import ShoppingCartSerializer


class ShoppingCartViewSet(mixins.CreateModelMixin,
                          mixins.DestroyModelMixin,
                          viewsets.GenericViewSet):
    """Работа со списком покупок."""
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'

    def perform_create(self, serializer):
        """Добавление в список покупок."""
        serializer.save(user=self.request.user,
                        recipe=Recipe.objects.get(id=self.kwargs['id']))

    def get_serializer(self, *args, **kwargs):
        """Изменение данных из запроса."""
        data = {'user': self.request.user.id, 'recipe': self.kwargs['id']}
        kwargs['data'] = data
        return super().get_serializer(*args, **kwargs)

    def get_queryset(self):
        """Получение кверисета для удаления."""
        queryset = super().get_queryset()
        recipe = get_object_or_404(Recipe, id=self.kwargs['id'])
        filtered_queryset = queryset.filter(user=self.request.user,
                                            recipe=recipe)
        return filtered_queryset

    def get_object(self):
        """Получение объекта для удаления."""
        queryset = self.get_queryset()
        if not queryset:
            raise ValidationError('Рецепта не существует.')
        return queryset.first()
