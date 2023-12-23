from django import forms


class RecipeForm(forms.ModelForm):
    """Форма для структуры ответа."""
    id = forms.IntegerField(required=True)
    tags = forms.CharField(required=True)
    author = forms.CharField(required=True)
    name = forms.CharField(required=True)
    ingredients = forms.CharField(required=True)
    is_favorited = forms.BooleanField(required=True)
    is_in_shopping_cart = forms.BooleanField(required=True)
    image = forms.ImageField(required=True)
    text = forms.CharField(required=True)
    cooking_time = forms.IntegerField(required=True)


class ArrayField(forms.CharField):
    """Собственное поля для формы подписок"""
    def to_char_to_array(self, value):
        """Преобразуем строку в массив."""
        if value:
            return [item.strip() for item in value.split(',')]
        return []


class FollowForm(forms.ModelForm):
    """Форма для структуры ответа."""
    id = forms.IntegerField(required=True)
    email = forms.EmailField(required=True)
    username = forms.CharField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    is_subscribed = forms.BooleanField(required=True)
    recipes = ArrayField(required=True)
    recipes_count = forms.IntegerField(required=True)
