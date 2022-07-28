from django.urls import include, path
from ingredients.views import IngredientViewSet
from recipes.views import TagViewSet
from rest_framework.routers import DefaultRouter
from users.views import CustomUserViewSet

from .views import RecipeViewSet

router = DefaultRouter()

router.register('tags', TagViewSet, basename='tag')
router.register('ingredients', IngredientViewSet, basename='ingredient')
router.register('recipes', RecipeViewSet, basename='recipe')
router.register('users', CustomUserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('api/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
