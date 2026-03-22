from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

from apps.references.models.mixins import TimeStampedMixin, UUIDMixin
from apps.references.models.status import Status
from apps.references.models.operation_type import OperationType
from apps.references.models.category import Category
from apps.references.models.subcategory import SubCategory


class CashflowRecord(TimeStampedMixin, UUIDMixin):
    record_date = models.DateField(
        default=timezone.now,
        # ускорит фильтрацию по дате
        db_index=True,
        verbose_name=_("Record date"),
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name=_("Amount"),
    )

    comment = models.TextField(
        blank=True,
        verbose_name=_("Comment"),
    )

    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        related_name="cashflow_records",
        verbose_name=_("Status"),
    )

    operation_type = models.ForeignKey(
        OperationType,
        on_delete=models.PROTECT,
        related_name="cashflow_records",
        verbose_name=_("Operation type"),
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="cashflow_records",
        verbose_name=_("Category"),
    )

    subcategory = models.ForeignKey(
        SubCategory,
        on_delete=models.PROTECT,
        related_name="cashflow_records",
        verbose_name=_("Subcategory"),
    )

    class Meta:
        verbose_name = _("Cashflow Record")
        verbose_name_plural = _("Cashflow Records")
        # сортировка по дате
        ordering = ("-record_date",)

    def clean(self):
        """
        Проверяет логические связи между типом операции, категорией
        и подкатегорией.

        Убеждается, что:
        - выбранная категория принадлежит выбранному типу операции;
        - выбранная подкатегория принадлежит выбранной категории.

        Raises:
            ValidationError: Если нарушены бизнес-правила связей.
        """
        super().clean()
        errors = {}

        if self.category_id and self.operation_type_id:
            if self.category.operation_type_id != self.operation_type_id:
                errors["category"] = _(
                    "Category does not belong to selected operation type."
                )

        if self.subcategory_id and self.category_id:
            if self.subcategory.category_id != self.category_id:
                errors["subcategory"] = _(
                    "Subcategory does not belong to selected category."
                )

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        """
        Выполняет полную валидацию модели перед сохранением в базу данных.
        """
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"{self.record_date} | {self.operation_type} |"
            f" {self.category}/{self.subcategory} | {self.amount}"
        )

    def __repr__(self):
        return f"<CashflowRecord id={self.id} amount={self.amount}>"
