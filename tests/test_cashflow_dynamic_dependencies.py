from decimal import Decimal

import pytest
from django.urls import reverse

from apps.references.models.category import Category
from apps.references.models.operation_type import OperationType
from apps.references.models.status import Status
from apps.references.models.subcategory import SubCategory
from apps.transactions.forms import CashflowRecordForm
from apps.transactions.models.cashflow_record import CashflowRecord


@pytest.fixture
def dependency_data():
    status = Status.objects.create(name="Бизнес")

    expense_type = OperationType.objects.create(name="Списание")
    income_type = OperationType.objects.create(name="Пополнение")

    infrastructure = Category.objects.create(
        name="Инфраструктура",
        operation_type=expense_type,
    )
    marketing = Category.objects.create(
        name="Маркетинг",
        operation_type=expense_type,
    )
    income_category = Category.objects.create(
        name="Прочее пополнение",
        operation_type=income_type,
    )

    proxy = SubCategory.objects.create(name="Proxy", category=infrastructure)
    vps = SubCategory.objects.create(name="VPS", category=infrastructure)
    farpost = SubCategory.objects.create(name="Farpost", category=marketing)
    income_subcategory = SubCategory.objects.create(
        name="Пополнение от клиента",
        category=income_category,
    )

    return {
        "status": status,
        "expense_type": expense_type,
        "income_type": income_type,
        "infrastructure": infrastructure,
        "marketing": marketing,
        "income_category": income_category,
        "proxy": proxy,
        "vps": vps,
        "farpost": farpost,
        "income_subcategory": income_subcategory,
    }


@pytest.mark.django_db
def test_categories_api_returns_only_categories_of_selected_operation_type(
    client,
    dependency_data,
):
    response = client.get(
        reverse("transactions:categories_by_operation_type"),
        {"operation_type_id": str(dependency_data["expense_type"].id)},
    )

    assert response.status_code == 200
    payload = response.json()
    names = [item["name"] for item in payload["results"]]

    assert names == ["Инфраструктура", "Маркетинг"]


@pytest.mark.django_db
def test_subcategories_api_returns_only_subcategories_of_selected_category(
    client,
    dependency_data,
):
    response = client.get(
        reverse("transactions:subcategories_by_category"),
        {"category_id": str(dependency_data["infrastructure"].id)},
    )

    assert response.status_code == 200
    payload = response.json()
    names = [item["name"] for item in payload["results"]]

    assert names == ["Proxy", "VPS"]


@pytest.mark.django_db
def test_dependency_apis_return_empty_for_invalid_ids(client):
    categories_response = client.get(
        reverse("transactions:categories_by_operation_type"),
        {"operation_type_id": "invalid-uuid"},
    )
    subcategories_response = client.get(
        reverse("transactions:subcategories_by_category"),
        {"category_id": "invalid-uuid"},
    )

    assert categories_response.status_code == 200
    assert categories_response.json() == {"results": []}

    assert subcategories_response.status_code == 200
    assert subcategories_response.json() == {"results": []}


@pytest.mark.django_db
def test_cashflow_form_limits_querysets_for_bound_data(dependency_data):
    form = CashflowRecordForm(
        data={
            "operation_type": str(dependency_data["expense_type"].id),
            "category": str(dependency_data["marketing"].id),
        }
    )

    expected_category_ids = list(
        Category.objects.filter(operation_type_id=dependency_data["expense_type"].id)
        .order_by("name")
        .values_list("id", flat=True)
    )
    actual_category_ids = list(
        form.fields["category"].queryset.values_list("id", flat=True)
    )

    expected_subcategory_ids = list(
        SubCategory.objects.filter(category_id=dependency_data["marketing"].id)
        .order_by("name")
        .values_list("id", flat=True)
    )
    actual_subcategory_ids = list(
        form.fields["subcategory"].queryset.values_list("id", flat=True)
    )

    assert actual_category_ids == expected_category_ids
    assert actual_subcategory_ids == expected_subcategory_ids


@pytest.mark.django_db
def test_cashflow_form_limits_querysets_for_instance(dependency_data):
    record = CashflowRecord.objects.create(
        record_date="2026-03-24",
        amount=Decimal("1500.00"),
        comment="Тест",
        status=dependency_data["status"],
        operation_type=dependency_data["expense_type"],
        category=dependency_data["infrastructure"],
        subcategory=dependency_data["proxy"],
    )

    form = CashflowRecordForm(instance=record)

    expected_category_ids = list(
        Category.objects.filter(operation_type_id=dependency_data["expense_type"].id)
        .order_by("name")
        .values_list("id", flat=True)
    )
    actual_category_ids = list(
        form.fields["category"].queryset.values_list("id", flat=True)
    )

    expected_subcategory_ids = list(
        SubCategory.objects.filter(category_id=dependency_data["infrastructure"].id)
        .order_by("name")
        .values_list("id", flat=True)
    )
    actual_subcategory_ids = list(
        form.fields["subcategory"].queryset.values_list("id", flat=True)
    )

    assert actual_category_ids == expected_category_ids
    assert actual_subcategory_ids == expected_subcategory_ids
