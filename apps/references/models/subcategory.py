from django.db import models
from django.utils.translation import gettext_lazy as _

from .mixins import TimeStampedMixin, UUIDMixin
from .category import Category


class SubCategory(TimeStampedMixin, UUIDMixin):
    name = models.CharField(
        max_length=64,
        verbose_name=_("Name"),
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="subcategories",
        verbose_name=_("Category"),
    )

    class Meta:
        verbose_name = _("Subcategory")
        verbose_name_plural = _("Subcategories")
        ordering = ("name",)

        # уникальность названия подкатегории в рамках одной категории
        constraints = [
            models.UniqueConstraint(
                fields=["category", "name"],
                name="unique_subcategory_name_per_category",
            )
        ]

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<SubCategory: {self.name}>"
