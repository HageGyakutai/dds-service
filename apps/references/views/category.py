from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from apps.references.models.category import Category
from apps.references.forms import CategoryForm


class CategoryListView(ListView):
    model = Category
    template_name = "references/category_list.html"
    context_object_name = "categories"


class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "references/form.html"
    success_url = reverse_lazy("references:category_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Create category")
        context["cancel_url"] = reverse_lazy("references:category_list")
        return context


class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = "references/form.html"
    success_url = reverse_lazy("references:category_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Update category")
        context["cancel_url"] = reverse_lazy("references:category_list")
        return context


class CategoryDeleteView(DeleteView):
    model = Category
    template_name = "references/confirm_delete.html"
    success_url = reverse_lazy("references:category_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Delete category")
        context["cancel_url"] = reverse_lazy("references:category_list")
        return context
