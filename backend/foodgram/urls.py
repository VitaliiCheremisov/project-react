from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from rest_framework.routers import DefaultRouter

from favorite.views import FavoriteViewSet
from recipes.views import FollowViewSet, IngredientViewSet, RecipeViewSet
from shopping_cart.views import ShoppingCartViewSet
from tags.views import TagViewSet
from users.views import CustomUserViewSet

router_v1 = DefaultRouter()
router_v1.register('users', CustomUserViewSet, basename='users')
router_v1.register('recipes', RecipeViewSet, basename='recipes')
router_v1.register('ingredients', IngredientViewSet, basename='ingredients')
router_v1.register('tags', TagViewSet, basename='tags')

api_patterns = [
    path('', include(router_v1.urls)),
    path('auth/', include('djoser.urls.authtoken')),
    path('recipes/<str:id>/favorite/',
         FavoriteViewSet.as_view({'post': 'create', 'delete': 'destroy'}),
         name='favorite'),
    path('users/<int:id>/subscribe/',
         FollowViewSet.as_view({'post': 'create', 'delete': 'destroy'}),
         name='subscribe'),
    path('recipes/<int:id>/shopping_cart/',
         ShoppingCartViewSet.as_view({'post': 'create', 'delete': 'destroy'}),
         name='shopping_cart'),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_patterns))
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
