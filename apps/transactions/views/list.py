from django.views.generic import ListView

from apps.transactions.models.cashflow_record import CashflowRecord


class CashflowRecordListView(ListView):
    model = CashflowRecord
    template_name = "transactions/list.html"
    context_object_name = "cashflow_records"
    paginate_by = 20
