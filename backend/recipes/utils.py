def calculate_shopping_cart(ingredients):
    """Расчет списка покупок."""
    shopping_list = []
    for ingredient in ingredients:
        shopping_list.append({
            'name': ingredient['ingredients__name'],
            'amount': ingredient['amounts'],
            'measurement_unit': ingredient['ingredients__measurement_unit']
        })
    return shopping_list
