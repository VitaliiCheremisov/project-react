def calculate_shopping_cart(ingredients):
    """Расчет списка покупок."""
    shopping_list = []
    for ingredient in ingredients:
        name = f"{ingredient['ingredients__name']}:"
        amount = f"{ingredient['amounts']}"
        unit = f"{ingredient['ingredients__measurement_unit']}"
        item = f"{name:<20} {amount:<10} {unit}"
        shopping_list.append(item)
    return shopping_list
