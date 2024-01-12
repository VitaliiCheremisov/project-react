from django.contrib import admin

from .forms import IngredientRecipesForm
from .models import Ingredient, IngredientRecipes, Recipe

admin.site.empty_value_display = '-пусто-'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)
    search_fields = ('name',)


class IngredientsInLine(admin.TabularInline):
    form = IngredientRecipesForm
    model = IngredientRecipes
    raw_id_fields = ('ingredients',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'name', 'count_favorite')
    search_fields = ('name',)
    list_filter = ('author', 'name', 'tags')
    inlines = (IngredientsInLine,)

    def count_favorite(self, obj):
        return obj.favorites.all().count()
