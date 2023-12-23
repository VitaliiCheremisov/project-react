from django.contrib import admin

from .models import Tag

admin.site.empty_value_display = '-пусто-'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    list_filter = ('name',)
    search_fields = ('name',)
