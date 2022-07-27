from rest_framework import viewsets

from api.filters import IngredientSearchFilter
from api.permissions import IsAdminOrReadOnly
from api.serializers import IngredientSerializer

from .models import Ingredient


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (IngredientSearchFilter,)
    search_fields = ('^name',)
