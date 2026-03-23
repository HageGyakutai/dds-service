from django.urls import reverse_lazy
from django.views.generic import UpdateView

from apps.transactions.models.cashflow_record import CashflowRecord
from apps.transactions.forms import CashflowRecordForm


class CashflowRecordUpdateView(UpdateView):
    model = CashflowRecord
    form_class = CashflowRecordForm
    template_name = "transactions/form.html"
    success_url = reverse_lazy("transactions:cashflow_record_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Редактирование записи о движении денежных средств"
        context["cancel_url"] = reverse_lazy("transactions:cashflow_record_list")
        return context
