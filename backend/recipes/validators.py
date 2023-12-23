from rest_framework.validators import ValidationError


def tags_validator(tags_data, Tag):
    """Провека тэгов."""
    if not tags_data:
        raise ValidationError('Нет тэгов')
    tags = Tag.objects.filter(id__in=tags_data)
    if len(tags) != len(tags_data):
        raise ValidationError('Указан несуществующий тэг')
    return tags


def ingredients_validator(ingredients_data, Ingredient):
    """Проверка ингредиентов."""
    if not ingredients_data:
        raise ValidationError('Не указаны ингредиенты')
    ingredients = Ingredient.objects.all()
    ingredients_stack = []
    ingredient_ids = [item['ingredients'].id for item in ingredients_stack]
    for ingredient_item in ingredients_data:
        try:
            ingredient = Ingredient.objects.get(id=ingredient_item['id'])
        except Ingredient.DoesNotExist:
            raise ValidationError('Такого ингредиента нет.')
        if ingredient.id in ingredient_ids:
            raise ValidationError(
                "Ингредиент уже добавлен в рецепт"
            )
        amount = ingredient_item['amount']
        if not (isinstance(ingredient_item['amount'], int)
                or ingredient_item['amount'].isdigit()):
            raise ValidationError('Неправильное количество ингидиента')
        if int(amount) < 1:
            raise ValidationError('Количество ингрединтов меньше 1')
        ingredients_stack.append({'ingredients': ingredient,
                                  'amount': amount
                                  })
        ingredient_ids.append(ingredient.id)
    ingredients = ingredients_stack
    return ingredients
