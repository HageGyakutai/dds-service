from django.utils.translation import gettext_lazy as _
from django.db import models
from .mixins import TimeStampedMixin, UUIDMixin


class Status(TimeStampedMixin, UUIDMixin):
    name = models.CharField(
        max_length=64,
        unique=True,
    )

    class Meta:
        verbose_name = _("Status")
        verbose_name_plural = _("Statuses")

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Status: {self.name}>"
