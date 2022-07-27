from rest_framework import viewsets

from api.permissions import IsAdminOrReadOnly
from api.serializers import TagSerializer

from .models import Tag


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)
