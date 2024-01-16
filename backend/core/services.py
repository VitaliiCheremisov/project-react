from django.core.management import call_command

from recipes.models import Ingredient


def import_ingredients_if_needed():
    """Проверяем наличие ингредиентов."""
    if Ingredient.objects.count() == 0:
        call_command('import_csv', 'ingredients.csv')
