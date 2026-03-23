from django.urls import path

from apps.references.views.index import ReferencesIndexView
from apps.references.views.status import (
    StatusCreateView,
    StatusDeleteView,
    StatusListView,
    StatusUpdateView,
)

from apps.references.views.operation_type import (
    OperationTypeCreateView,
    OperationTypeDeleteView,
    OperationTypeListView,
    OperationTypeUpdateView,
)

from apps.references.views.category import (
    CategoryCreateView,
    CategoryDeleteView,
    CategoryListView,
    CategoryUpdateView,
)

from apps.references.views.subcategory import (
    SubCategoryCreateView,
    SubCategoryDeleteView,
    SubCategoryListView,
    SubCategoryUpdateView,
)

app_name = "references"

urlpatterns = [
    path("", ReferencesIndexView.as_view(), name="index"),
    path("statuses/", StatusListView.as_view(), name="status_list"),
    path("statuses/create/", StatusCreateView.as_view(), name="status_create"),
    path(
        "statuses/<uuid:pk>/update/", StatusUpdateView.as_view(), name="status_update"
    ),
    path(
        "statuses/<uuid:pk>/delete/", StatusDeleteView.as_view(), name="status_delete"
    ),
    path(
        "operation-types/", OperationTypeListView.as_view(), name="operation_type_list"
    ),
    path(
        "operation-types/create/",
        OperationTypeCreateView.as_view(),
        name="operation_type_create",
    ),
    path(
        "operation-types/<uuid:pk>/update/",
        OperationTypeUpdateView.as_view(),
        name="operation_type_update",
    ),
    path(
        "operation-types/<uuid:pk>/delete/",
        OperationTypeDeleteView.as_view(),
        name="operation_type_delete",
    ),
    path("categories/", CategoryListView.as_view(), name="category_list"),
    path("categories/create/", CategoryCreateView.as_view(), name="category_create"),
    path(
        "categories/<uuid:pk>/update/",
        CategoryUpdateView.as_view(),
        name="category_update",
    ),
    path(
        "categories/<uuid:pk>/delete/",
        CategoryDeleteView.as_view(),
        name="category_delete",
    ),
    path("subcategories/", SubCategoryListView.as_view(), name="subcategory_list"),
    path(
        "subcategories/create/",
        SubCategoryCreateView.as_view(),
        name="subcategory_create",
    ),
    path(
        "subcategories/<uuid:pk>/update/",
        SubCategoryUpdateView.as_view(),
        name="subcategory_update",
    ),
    path(
        "subcategories/<uuid:pk>/delete/",
        SubCategoryDeleteView.as_view(),
        name="subcategory_delete",
    ),
]
