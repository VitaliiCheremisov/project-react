def calculate_shopping_cart(ingredients):
    """Расчет списка покупок."""
    shopping_list = []
    for ingredient in ingredients:
        item = (f"{ingredient['ingredients__name']}: "
                f"{ingredient['amounts']} "
                f"{ingredient['ingredients__measurement_unit']}")
        shopping_list.append(item)
    return shopping_list
