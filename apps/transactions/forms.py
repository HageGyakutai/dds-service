import uuid

from django import forms
from django.utils.translation import gettext_lazy as _

from apps.references.models.category import Category
from apps.references.models.subcategory import SubCategory
from apps.transactions.models.cashflow_record import CashflowRecord


def _parse_uuid(value: str | None) -> uuid.UUID | None:
    if not value:
        return None
    try:
        return uuid.UUID(value)
    except (ValueError, TypeError):
        return None


class CashflowRecordForm(forms.ModelForm):
    class Meta:
        model = CashflowRecord
        fields = [
            "record_date",
            "amount",
            "comment",
            "status",
            "operation_type",
            "category",
            "subcategory",
        ]
        labels = {
            "record_date": _("Date"),
            "amount": _("Amount"),
            "comment": _("Comment"),
            "status": _("Status"),
            "operation_type": _("Operation type"),
            "category": _("Category"),
            "subcategory": _("Subcategory"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["category"].queryset = Category.objects.none()
        self.fields["subcategory"].queryset = SubCategory.objects.none()

        operation_type_id = self._get_operation_type_id()
        if operation_type_id:
            self.fields["category"].queryset = Category.objects.filter(
                operation_type_id=operation_type_id
            ).order_by("name")

        category_id = self._get_category_id()
        if category_id:
            self.fields["subcategory"].queryset = SubCategory.objects.filter(
                category_id=category_id
            ).order_by("name")

    def _get_operation_type_id(self) -> uuid.UUID | None:
        if self.is_bound:
            return _parse_uuid(self.data.get("operation_type"))
        if self.instance and self.instance.pk and self.instance.operation_type_id:
            return self.instance.operation_type_id
        return None

    def _get_category_id(self) -> uuid.UUID | None:
        if self.is_bound:
            return _parse_uuid(self.data.get("category"))
        if self.instance and self.instance.pk and self.instance.category_id:
            return self.instance.category_id
        return None

    def clean(self):
        cleaned_data = super().clean()

        operation_type = cleaned_data.get("operation_type")
        category = cleaned_data.get("category")
        subcategory = cleaned_data.get("subcategory")

        if operation_type and category:
            if category.operation_type_id != operation_type.id:
                self.add_error(
                    "category",
                    _("Selected category does not belong to the chosen operation type."),
                )

        if category and subcategory:
            if subcategory.category_id != category.id:
                self.add_error(
                    "subcategory",
                    _("Selected subcategory does not belong to the chosen category."),
                )

        return cleaned_data
