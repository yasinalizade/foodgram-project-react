from django.urls import include, path
from rest_framework.routers import DefaultRouter

from recipes.views import TagViewSet
from ingredients.views import IngredientViewSet
from users.views import CustomUserViewSet
from .views import RecipeViewSet

router = DefaultRouter()

router.register('tags', TagViewSet, basename='tag')
router.register('ingredients', IngredientViewSet, basename='ingredient')
router.register('recipes', RecipeViewSet, basename='recipe')
router.register('users', CustomUserViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include('djoser.urls')),
    path('v1/auth/', include('djoser.urls.authtoken')),
]
