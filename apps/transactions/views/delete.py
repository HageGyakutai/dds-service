from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import DeleteView

from apps.transactions.models.cashflow_record import CashflowRecord


class CashflowRecordDeleteView(DeleteView):
    model = CashflowRecord
    template_name = "transactions/confirm_delete.html"
    success_url = reverse_lazy("transactions:cashflow_record_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Удаление записи ДДС"
        context["cancel_url"] = reverse_lazy("transactions:cashflow_record_list")
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Запись ДДС удалена.")
        return response
