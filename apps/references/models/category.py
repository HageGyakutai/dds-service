from django.db import models
from django.utils.translation import gettext_lazy as _

from .mixins import TimeStampedMixin, UUIDMixin
from .operation_type import OperationType


class Category(TimeStampedMixin, UUIDMixin):
    name = models.CharField(
        max_length=64,
        verbose_name=_("Name"),
    )
    operation_type = models.ForeignKey(
        OperationType,
        on_delete=models.PROTECT,
        related_name="categories",
        verbose_name=_("Operation type"),
    )

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ("name",)

        # уникальность названия категории в рамках одного типа операции
        constraints = [
            models.UniqueConstraint(
                fields=["operation_type", "name"],
                name="unique_category_name_per_operation_type",
            )
        ]

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Category: {self.name}>"
