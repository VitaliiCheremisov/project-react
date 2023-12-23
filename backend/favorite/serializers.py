from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from drf_extra_fields.fields import Base64ImageField

from .models import Favorite


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериалайзер для избранного."""
    name = serializers.CharField()
    image = Base64ImageField()
    cooking_time = serializers.IntegerField()

    class Meta:
        model = Favorite
        fields = ('id', 'name', 'image', 'cooking_time')
        validators = UniqueTogetherValidator(
            queryset=Favorite.objects.all(),
            fields=('user', 'recipe')
        )
