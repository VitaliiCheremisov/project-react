def calculate_shopping_cart(ingredients):
    """Расчет списка покупок."""
    shopping_list = []
    max_length_name = max([len(ingredient['ingredients__name'])
                           for ingredient in ingredients])
    max_length_amount = max([len(str(ingredient['amounts']))
                             for ingredient in ingredients])
    for ingredient in ingredients:
        name = f"{ingredient['ingredients__name']}".ljust(max_length_name + 2)
        amount = f"{ingredient['amounts']}".ljust(max_length_amount + 2)
        unit = f"{ingredient['ingredients__measurement_unit']}"
        item = f"{name}{amount}{unit}\n"
        shopping_list.append(item)
    return ''.join(shopping_list)
