from django.db import models
from django.utils.translation import gettext_lazy as _

from .mixins import TimeStampedMixin, UUIDMixin


class OperationType(TimeStampedMixin, UUIDMixin):
    name = models.CharField(
        max_length=64,
        unique=True,
        verbose_name=_("Name"),
    )

    class Meta:
        verbose_name = _("Operation Type")
        verbose_name_plural = _("Operation Types")
        ordering = ("name",)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<OperationType: {self.name}>"
