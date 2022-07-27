from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Subscription(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribe_to',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriber',
    )

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['author', 'user'], name='unique_follower')
        ]
        verbose_name = _('Subscription')
        verbose_name_plural = _('Subscriptions')

    def __str__(self) -> str:
        return f'{self.user} follows {self.author}'
