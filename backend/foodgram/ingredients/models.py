from django.db import models
from django.utils.translation import gettext_lazy as _


class Ingredient(models.Model):
    """
    Model describes ingredients for recipes.
    Relation ManyToMany.
    """

    name = models.CharField(
        _('Name'),
        max_length=200,
        db_index=True,
        blank=False,
    )
    measurement_unit = models.CharField(
        _('Measurement unit'),
        max_length=200,
        blank=False,
    )

    class Meta:
        ordering = ('name',)
        verbose_name = _('Ingredient')
        verbose_name_plural = _('Ingredients')

    def __str__(self) -> str:
        return self.name
