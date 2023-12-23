from rest_framework import serializers

from .models import Tag


class TagSerializer(serializers.ModelSerializer):
    """Сериалайзер для тэгов."""

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')
        read_only_fields = ('id', 'name', 'color', 'slug')

    def to_internal_value(self, data):
        if isinstance(data, int):
            return {'id': data}
        return super().to_internal_value(data)
