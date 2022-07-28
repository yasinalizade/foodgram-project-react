from api.permissions import IsAdminOrReadOnly
from api.serializers import TagSerializer
from rest_framework import viewsets

from .models import Tag


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)
