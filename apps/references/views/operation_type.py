from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from apps.references.models.operation_type import OperationType
from apps.references.forms import OperationTypeForm


class OperationTypeListView(ListView):
    model = OperationType
    template_name = "references/operation_type_list.html"
    context_object_name = "operation_types"


class OperationTypeCreateView(CreateView):
    model = OperationType
    form_class = OperationTypeForm
    template_name = "references/form.html"
    success_url = reverse_lazy("references:operation_type_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Create operation type")
        context["cancel_url"] = reverse_lazy("references:operation_type_list")
        return context


class OperationTypeUpdateView(UpdateView):
    model = OperationType
    form_class = OperationTypeForm
    template_name = "references/form.html"
    success_url = reverse_lazy("references:operation_type_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Update operation type")
        context["cancel_url"] = reverse_lazy("references:operation_type_list")
        return context


class OperationTypeDeleteView(DeleteView):
    model = OperationType
    template_name = "references/confirm_delete.html"
    success_url = reverse_lazy("references:operation_type_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Delete operation type")
        context["cancel_url"] = reverse_lazy("references:operation_type_list")
        return context
