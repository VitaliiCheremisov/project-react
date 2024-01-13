from tabulate import tabulate


def calculate_shopping_cart(ingredients):
    """Расчет списка покупок."""
    shopping_list = []
    for ingredient in ingredients:
        name = f"{ingredient['ingredients__name']}"
        amount = f"{ingredient['amounts']}"
        unit = f"{ingredient['ingredients__measurement_unit']}"
        item = [name, amount, unit]
        shopping_list.append(item)
    return tabulate(shopping_list,
                    headers=["Ингредиент", "Количество", "Единица измерения"],
                    tablefmt='grid')
