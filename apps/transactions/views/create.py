from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView

from apps.transactions.models.cashflow_record import CashflowRecord
from apps.transactions.forms import CashflowRecordForm


class CashflowRecordCreateView(CreateView):
    model = CashflowRecord
    form_class = CashflowRecordForm
    template_name = "transactions/form.html"
    success_url = reverse_lazy("transactions:cashflow_record_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Create cashflow record")
        context["cancel_url"] = reverse_lazy("transactions:cashflow_record_list")
        return context
