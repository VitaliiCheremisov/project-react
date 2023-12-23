from django.db.models import Q
from rest_framework.filters import SearchFilter

import django_filters
from django_filters.rest_framework import FilterSet, filters

from recipes.models import Recipe
from users.models import CustomUser


class IngredientSearchFilter(SearchFilter):
    """Фильтр для поиска ингредиентов по названию."""
    search_param = 'name'


class TagFilter(django_filters.Filter):
    """Фильтр для тэгов."""
    def filter(self, queryset, value):
        if value:
            tags = value.split(',')
            query = Q()
            for tag in tags:
                query |= Q(tags__name=tag)
            return queryset.filter(query)
        return queryset


class RecipeFilter(FilterSet):
    """Фильтр для рецептов."""
    author = filters.ModelChoiceFilter(
        queryset=CustomUser.objects.all()
    )
    tags = filters.AllValuesMultipleFilter(
        field_name='tags__slug'
    )
    is_favorited = filters.BooleanFilter(
        method='filter_is_favorited'
    )
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = ('author', 'tags', 'is_favorited', 'is_in_shopping_cart')

    def filter_is_favorited(self, queryset, value, name):
        """Метод фильтрации по наличию в избранном."""
        if self.request.user.is_authenticated and value:
            return queryset.filter(favorite__user=self.request.user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, value, name):
        """Метод фильтрации списка покупок."""
        if self.request.user.is_authenticated and value:
            return queryset.filter(shopping_cart__user=self.request.user)
        return queryset
