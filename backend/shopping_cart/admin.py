from django.contrib import admin

from .models import ShoppingCart

admin.site.empty_value_display = '-пусто-'


@admin.register(ShoppingCart)
class BuyingListAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    list_filter = ('user',)
    search_fields = ('user',)
