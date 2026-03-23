from django.views.generic import ListView

from apps.transactions.filters import CashflowRecordFilter
from apps.transactions.models.cashflow_record import CashflowRecord


class CashflowRecordListView(ListView):
    model = CashflowRecord
    template_name = "transactions/list.html"
    context_object_name = "cashflow_records"
    paginate_by = 20

    def get_base_queryset(self):
        return CashflowRecord.objects.select_related(
            "status",
            "operation_type",
            "category",
            "subcategory",
        )

    def get_filterset(self):
        return CashflowRecordFilter(self.request.GET, queryset=self.get_base_queryset())

    def get_queryset(self):
        return self.get_filterset().qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = self.get_filterset()
        context["has_records"] = CashflowRecord.objects.exists()

        query_params = self.request.GET.copy()
        query_params.pop("page", None)
        context["querystring"] = query_params.urlencode()

        return context
