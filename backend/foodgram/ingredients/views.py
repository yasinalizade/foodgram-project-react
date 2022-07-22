from rest_framework import viewsets

from .models import Ingredient
from api.serializers import IngredientSerializer
from api.permissions import IsAdminOrReadOnly


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminOrReadOnly,)
