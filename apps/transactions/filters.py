import django_filters

from apps.references.models.category import Category
from apps.references.models.operation_type import OperationType
from apps.references.models.status import Status
from apps.references.models.subcategory import SubCategory
from apps.transactions.models.cashflow_record import CashflowRecord


class CashflowRecordFilter(django_filters.FilterSet):
    date_from = django_filters.DateFilter(
        field_name="record_date",
        lookup_expr="gte",
        label="Дата от",
    )
    date_to = django_filters.DateFilter(
        field_name="record_date",
        lookup_expr="lte",
        label="Дата до",
    )
    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all(),
        label="Статус",
    )
    operation_type = django_filters.ModelChoiceFilter(
        queryset=OperationType.objects.all(),
        label="Тип операции",
    )
    category = django_filters.ModelChoiceFilter(
        queryset=Category.objects.all(),
        label="Категория",
    )
    subcategory = django_filters.ModelChoiceFilter(
        queryset=SubCategory.objects.all(),
        label="Подкатегория",
    )

    class Meta:
        model = CashflowRecord
        fields = [
            "status",
            "operation_type",
            "category",
            "subcategory",
        ]
