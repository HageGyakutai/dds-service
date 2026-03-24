from decimal import Decimal

import pytest
from django.urls import reverse

from apps.references.models.category import Category
from apps.references.models.operation_type import OperationType
from apps.references.models.status import Status
from apps.references.models.subcategory import SubCategory
from apps.transactions.models.cashflow_record import CashflowRecord


@pytest.fixture
def references_data():
    """Создаёт минимальный набор справочников для тестов создания записи ДДС."""
    status = Status.objects.create(name="Бизнес")

    income_type = OperationType.objects.create(name="Пополнение")
    expense_type = OperationType.objects.create(name="Списание")

    infrastructure = Category.objects.create(
        name="Инфраструктура",
        operation_type=expense_type,
    )
    marketing = Category.objects.create(
        name="Маркетинг",
        operation_type=expense_type,
    )

    proxy = SubCategory.objects.create(name="Proxy", category=infrastructure)
    farpost = SubCategory.objects.create(name="Farpost", category=marketing)

    return {
        "status": status,
        "income_type": income_type,
        "expense_type": expense_type,
        "infrastructure": infrastructure,
        "marketing": marketing,
        "proxy": proxy,
        "farpost": farpost,
    }


@pytest.mark.django_db
def test_cashflow_create_page_returns_ok(client):
    response = client.get(reverse("transactions:cashflow_record_create"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_cashflow_create_saves_valid_record(client, references_data):
    response = client.post(
        reverse("transactions:cashflow_record_create"),
        data={
            "record_date": "2026-03-24",
            "amount": "2500.00",
            "comment": "Новая запись",
            "status": str(references_data["status"].pk),
            "operation_type": str(references_data["expense_type"].pk),
            "category": str(references_data["infrastructure"].pk),
            "subcategory": str(references_data["proxy"].pk),
        },
    )

    assert response.status_code == 302
    assert CashflowRecord.objects.count() == 1

    record = CashflowRecord.objects.get()
    assert record.record_date.isoformat() == "2026-03-24"
    assert record.amount == Decimal("2500.00")
    assert record.comment == "Новая запись"
    assert record.status_id == references_data["status"].id
    assert record.operation_type_id == references_data["expense_type"].id
    assert record.category_id == references_data["infrastructure"].id
    assert record.subcategory_id == references_data["proxy"].id


@pytest.mark.django_db
def test_cashflow_create_rejects_category_from_wrong_operation_type(
    client,
    references_data,
):
    response = client.post(
        reverse("transactions:cashflow_record_create"),
        data={
            "record_date": "2026-03-24",
            "amount": "2500.00",
            "comment": "Невалидная запись",
            "status": str(references_data["status"].pk),
            "operation_type": str(references_data["income_type"].pk),
            "category": str(references_data["infrastructure"].pk),
            "subcategory": str(references_data["proxy"].pk),
        },
    )

    assert response.status_code == 200
    assert CashflowRecord.objects.count() == 0
    assert "category" in response.context["form"].errors


@pytest.mark.django_db
def test_cashflow_create_rejects_subcategory_from_wrong_category(
    client,
    references_data,
):
    response = client.post(
        reverse("transactions:cashflow_record_create"),
        data={
            "record_date": "2026-03-24",
            "amount": "2500.00",
            "comment": "Невалидная запись",
            "status": str(references_data["status"].pk),
            "operation_type": str(references_data["expense_type"].pk),
            "category": str(references_data["infrastructure"].pk),
            "subcategory": str(references_data["farpost"].pk),
        },
    )

    assert response.status_code == 200
    assert CashflowRecord.objects.count() == 0
    assert "subcategory" in response.context["form"].errors
