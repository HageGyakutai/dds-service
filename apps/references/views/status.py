from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from apps.references.models.status import Status
from apps.references.forms import StatusForm


class StatusListView(ListView):
    model = Status
    template_name = "references/status_list.html"
    context_object_name = "statuses"


class StatusCreateView(CreateView):
    model = Status
    form_class = StatusForm
    template_name = "references/form.html"
    success_url = reverse_lazy("references:status_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Create status")
        context["cancel_url"] = reverse_lazy("references:status_list")
        return context


class StatusUpdateView(UpdateView):
    model = Status
    form_class = StatusForm
    template_name = "references/form.html"
    success_url = reverse_lazy("references:status_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Update status")
        context["cancel_url"] = reverse_lazy("references:status_list")
        return context


class StatusDeleteView(DeleteView):
    model = Status
    template_name = "references/confirm_delete.html"
    success_url = reverse_lazy("references:status_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Delete status")
        context["cancel_url"] = reverse_lazy("references:status_list")
        return context
