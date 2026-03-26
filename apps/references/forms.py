from django import forms
from django.utils.translation import gettext_lazy as _

from apps.references.models.category import Category
from apps.references.models.operation_type import OperationType
from apps.references.models.status import Status
from apps.references.models.subcategory import SubCategory


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "operation_type"]
        labels = {
            "name": _("Name"),
            "operation_type": _("Operation type"),
        }


class OperationTypeForm(forms.ModelForm):
    class Meta:
        model = OperationType
        fields = ["name"]
        labels = {
            "name": _("Name"),
        }


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ["name"]
        labels = {
            "name": _("Name"),
        }


class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = ["name", "category"]
        labels = {
            "name": _("Name"),
            "category": _("Category"),
        }
