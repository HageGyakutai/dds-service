from django import forms

from apps.references.models.category import Category
from apps.references.models.operation_type import OperationType
from apps.references.models.status import Status
from apps.references.models.subcategory import SubCategory


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "operation_type"]


class OperationTypeForm(forms.ModelForm):
    class Meta:
        model = OperationType
        fields = ["name"]


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ["name"]


class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = ["name", "category"]
