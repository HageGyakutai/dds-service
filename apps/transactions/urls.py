from django.urls import path

from apps.transactions.views.create import CashflowRecordCreateView
from apps.transactions.views.list import CashflowRecordListView
from apps.transactions.views.update import CashflowRecordUpdateView
from apps.transactions.views.delete import CashflowRecordDeleteView
from apps.transactions.views.dependencies import (
    CategoriesByOperationTypeView,
    SubCategoriesByCategoryView,
)


app_name = "transactions"

urlpatterns = [
    path("", CashflowRecordListView.as_view(), name="cashflow_record_list"),
    path("create/", CashflowRecordCreateView.as_view(), name="cashflow_record_create"),
    path(
        "<uuid:pk>/update/",
        CashflowRecordUpdateView.as_view(),
        name="cashflow_record_update",
    ),
    path(
        "<uuid:pk>/delete/",
        CashflowRecordDeleteView.as_view(),
        name="cashflow_record_delete",
    ),
    path(
        "api/categories/",
        CategoriesByOperationTypeView.as_view(),
        name="categories_by_operation_type",
    ),
    path(
        "api/subcategories/",
        SubCategoriesByCategoryView.as_view(),
        name="subcategories_by_category",
    ),
]
