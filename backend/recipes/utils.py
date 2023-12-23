from django.db.models import Sum
from django.http import HttpResponse

from .models import IngredientRecipes


def calculate_shopping_cart(self, request, author):
    """Расчет списка покупок."""
    ingredients_in_recipes = IngredientRecipes.objects.filter(
        recipes__shopping_cart__user=author
    ).values(
        'ingredients__name', 'ingredients__measurement_unit'
    ).annotate(amounts=Sum('amount', distinct=True)).order_by('amounts')
    shopping_list = ''
    for ingredient in ingredients_in_recipes:
        shopping_list += (
            f'{ingredient["ingredients__name"]} - '
            f'{ingredient["amounts"]} '
            f'{ingredient["ingredients__measurement_unit"]}'
        )
    response = HttpResponse(shopping_list, content_type='text/plain')
    response['Content-Disposition'] = ('attachment; '
                                       'filename="shopping_list.txt"')
    return response
