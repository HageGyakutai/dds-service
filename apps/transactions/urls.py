from django.urls import path

from apps.transactions.views.create import CashflowRecordCreateView
from apps.transactions.views.list import CashflowRecordListView
from apps.transactions.views.update import CashflowRecordUpdateView


app_name = "transactions"

urlpatterns = [
    path("", CashflowRecordListView.as_view(), name="cashflow_record_list"),
    path("create/", CashflowRecordCreateView.as_view(), name="cashflow_record_create"),
    path(
        "<uuid:pk>/update/",
        CashflowRecordUpdateView.as_view(),
        name="cashflow_record_update",
    ),
]
