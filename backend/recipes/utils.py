def calculate_shopping_cart(ingredients):
    """Расчет списка покупок."""
    shopping_list = []
    for ingredient in ingredients:
        item = f"{ingredient['ingredients__name']}: {ingredient['amounts']} {ingredient['ingredients__measurement_unit']}"
        shopping_list.append(item)
    return shopping_list
