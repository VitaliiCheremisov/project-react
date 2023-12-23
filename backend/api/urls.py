from django.urls import include, path
from favorite.views import FavoriteViewSet
from recipes.views import FollowViewSet, IngredientViewSet, RecipeViewSet
from rest_framework.routers import DefaultRouter
from shopping_cart.views import ShoppingCartViewSet
from tags.views import TagViewSet
from users.views import CustomUserViewSet

app_name = 'api'


router_v1 = DefaultRouter()
router_v1.register('users', CustomUserViewSet, basename='users')
router_v1.register('recipes', RecipeViewSet, basename='recipes')
router_v1.register('ingredients', IngredientViewSet, basename='ingredients')
router_v1.register('tags', TagViewSet, basename='tags')

urlpatterns = [
    path('', include(router_v1.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('recipes/<str:id>/favorite/',
         FavoriteViewSet.as_view({'post': 'create', 'delete': 'delete'}),
         name='favorite'),
    path('users/<int:id>/subscribe/',
         FollowViewSet.as_view({'post': 'create', 'delete': 'delete'}),
         name='subscribe'),
    path('recipes/<int:id>/shopping_cart/',
         ShoppingCartViewSet.as_view({'post': 'create', 'delete': 'delete'}),
         name='shopping_cart'),
]
