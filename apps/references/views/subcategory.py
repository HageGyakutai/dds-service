from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from apps.references.models.subcategory import SubCategory
from apps.references.forms import SubCategoryForm


class SubCategoryListView(ListView):
    model = SubCategory
    template_name = "references/subcategory_list.html"
    context_object_name = "subcategories"


class SubCategoryCreateView(CreateView):
    model = SubCategory
    form_class = SubCategoryForm
    template_name = "references/form.html"
    success_url = reverse_lazy("references:subcategory_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Создание подкатегории"
        context["cancel_url"] = reverse_lazy("references:subcategory_list")
        return context


class SubCategoryUpdateView(UpdateView):
    model = SubCategory
    form_class = SubCategoryForm
    template_name = "references/form.html"
    success_url = reverse_lazy("references:subcategory_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Редактирование подкатегории"
        context["cancel_url"] = reverse_lazy("references:subcategory_list")
        return context


class SubCategoryDeleteView(DeleteView):
    model = SubCategory
    template_name = "references/confirm_delete.html"
    success_url = reverse_lazy("references:subcategory_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Удаление подкатегории"
        context["cancel_url"] = reverse_lazy("references:subcategory_list")
        return context
