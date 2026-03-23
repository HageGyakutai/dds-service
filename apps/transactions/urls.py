from django.urls import path

from apps.transactions.views.create import CashflowRecordCreateView
from apps.transactions.views.list import CashflowRecordListView


app_name = "transactions"

urlpatterns = [
    path("", CashflowRecordListView.as_view(), name="cashflow_record_list"),
    path("create/", CashflowRecordCreateView.as_view(), name="cashflow_record_create"),
]
