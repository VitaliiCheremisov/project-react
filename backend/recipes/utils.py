def calculate_shopping_cart(ingredients):
    """Расчет списка покупок."""
    shopping_list = ''
    for ingredient in ingredients:
        shopping_list += (
            f'{ingredient["ingredients__name"]} - '
            f'{ingredient["amounts"]} '
            f'{ingredient["ingredients__measurement_unit"]}'
        )
    return shopping_list
