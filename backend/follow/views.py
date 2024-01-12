from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ValidationError

from .models import Follow
from .serializers import FollowSerializer

CustomUser = get_user_model()


class FollowViewSet(viewsets.ModelViewSet):
    """Работа с подписками пользователя."""

    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'

    def perform_create(self, serializer):
        """Создание подписки."""
        serializer.save(user=self.request.user,
                        author=get_object_or_404(
                            CustomUser,
                            id=self.kwargs['id'])
                        )

    def get_queryset(self):
        """Получение кверисета для удаления."""
        queryset = super().get_queryset()
        author = get_object_or_404(CustomUser, id=self.kwargs['id'])
        filtered_queryset = queryset.filter(user=self.request.user,
                                            author=author)
        return filtered_queryset

    def get_object(self):
        """Получение объекта для удаления"""
        queryset = self.get_queryset()
        if not queryset:
            raise ValidationError('Подписки не существует')
        return queryset.first()
