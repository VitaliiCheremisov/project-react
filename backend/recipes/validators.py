from django.db import models
from django.shortcuts import get_object_or_404

from rest_framework.validators import ValidationError


def tags_validator(tags_data, Tag):
    """Проверка тэгов."""
    if isinstance(tags_data, models.QuerySet):
        tags_ids = [tag.id for tag in tags_data]
    elif (isinstance(tags_data, list)
          and all(isinstance(item, Tag) for item in tags_data)):
        tags_ids = [tag.id for tag in tags_data]
    elif (isinstance(tags_data, list)
          and all(isinstance(item, dict) for item in tags_data)):
        tags_ids = [tag['id'] for tag in tags_data]
    else:
        raise ValidationError('Некорректный формат тэгов')
    if not tags_ids:
        raise ValidationError('Нет тэгов')
    tags = Tag.objects.filter(id__in=tags_ids)
    if len(tags) != len(tags_ids):
        raise ValidationError('Указан несуществующий тэг')
    return tags


def ingredients_validator(ingredients_data, Ingredient):
    """Проверка ингредиентов."""
    if not ingredients_data:
        raise ValidationError('Не указаны ингредиенты')
    ingredients_stack = []
    for item in ingredients_data:
        ingredient = get_object_or_404(Ingredient, name=item['id'])
        if ingredient in ingredients_stack:
            raise ValidationError(
                "Ингредиент уже добавлен в рецепт"
            )
        if int(item['amount']) < 1:
            raise ValidationError('Количество ингрединтов меньше 1')
        ingredients_stack.append(ingredient)
    return ingredients_data
