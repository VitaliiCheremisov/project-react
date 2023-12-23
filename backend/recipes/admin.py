from django.contrib import admin

from .forms import FollowForm, RecipeForm
from .models import Follow, Ingredient, IngredientRecipes, Recipe

admin.site.empty_value_display = '-пусто-'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)
    search_fields = ('name',)


class IngredientsInLine(admin.TabularInline):
    model = IngredientRecipes
    raw_id_fields = ('ingredients',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    form = RecipeForm
    list_display = ('id', 'author', 'name')
    search_fields = ('name',)
    list_filter = ('author', 'name', 'tags')
    inlines = (IngredientsInLine,)

    def count_favorite(self, obj):
        return obj.favorite.all().count()


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    form = FollowForm
    list_display = ('author', 'user')
    search_fields = ('user',)
    list_filter = ('user',)
