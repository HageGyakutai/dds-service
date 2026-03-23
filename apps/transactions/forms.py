from django import forms

from apps.transactions.models.cashflow_record import CashflowRecord


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

    def clean(self):
        cleaned_data = super().clean()

        operation_type = cleaned_data.get("operation_type")
        category = cleaned_data.get("category")
        subcategory = cleaned_data.get("subcategory")

        if operation_type and category:
            if category.operation_type_id != operation_type.id:
                self.add_error(
                    "category",
                    "Выбранная категория не относится к указанному типу операции.",
                )

        if category and subcategory:
            if subcategory.category_id != category.id:
                self.add_error(
                    "subcategory",
                    "Выбранная подкатегория не относится к указанной категории.",
                )

        return cleaned_data
