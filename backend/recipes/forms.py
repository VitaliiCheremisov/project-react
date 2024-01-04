from django import forms

from .models import IngredientRecipes


class IngredientRecipesForm(forms.ModelForm):
    """Форма для инлайн элемента."""
    class Meta:
        model = IngredientRecipes
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.vaules():
            field.required = True
