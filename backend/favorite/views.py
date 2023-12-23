from rest_framework import status, viewsets
from rest_framework.response import Response

from api.permissions import IsAuthenticatedOrDelete
from recipes.models import Recipe

from .models import Favorite
from .serializers import FavoriteSerializer


class FavoriteViewSet(viewsets.ModelViewSet):
    """Работа с избранными рецептами."""

    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = (IsAuthenticatedOrDelete,)

    def create(self, request, *args, **kwargs):
        """Добавление рецепта в избранное."""
        try:
            recipe = Recipe.objects.get(id=self.kwargs['id'])
        except Recipe.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if Favorite.objects.filter(user=request.user, recipe=recipe).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        Favorite.objects.create(user=request.user, recipe=recipe)
        serializer = FavoriteSerializer()
        return Response(
            serializer.to_representation(instance=recipe),
            status=status.HTTP_201_CREATED,
        )

    def delete(self, request, *args, **kwargs):
        """Удаление рецепта из избранного"""
        if self.request.user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if not Recipe.objects.filter(
            id=self.kwargs['id']
        ).exists():
            return Response(status=status.HTTP_404_NOT_FOUND)
        if not Favorite.objects.filter(
            user=request.user,
            recipe__id=int(self.kwargs['id'])
        ).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        Favorite.objects.filter(
            user__id=request.user.id, recipe__id=int(self.kwargs['id'])
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
