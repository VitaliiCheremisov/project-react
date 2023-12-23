from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Tag
from .serializers import TagSerializer


class TagViewSet(mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    """Работа с тэгами."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)

    def list(self, request, *args, **kwargs):
        """Убираем дополнительную информацию в ответе api."""
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
