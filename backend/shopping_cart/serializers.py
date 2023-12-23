from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from drf_extra_fields.fields import Base64ImageField

from .models import ShoppingCart


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Сериайлайзер для списка покупок."""
    id = serializers.IntegerField()
    name = serializers.CharField()
    image = Base64ImageField()
    cooking_time = serializers.IntegerField()

    class Meta:
        model = ShoppingCart
        fields = ('id', 'name', 'image', 'cooking_time')
        validators = [
            UniqueTogetherValidator(
                queryset=ShoppingCart.objects.all(),
                fields=('user', 'recipes')
            )
        ]
