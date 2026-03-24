from decimal import Decimal

import pytest
from django.contrib.messages import get_messages
from django.urls import reverse

from apps.references.models.category import Category
from apps.references.models.operation_type import OperationType
from apps.references.models.status import Status
from apps.references.models.subcategory import SubCategory
from apps.transactions.models.cashflow_record import CashflowRecord


@pytest.fixture
def references_data():
    status = Status.objects.create(name="Бизнес")
    operation_type = OperationType.objects.create(name="Списание")
    category = Category.objects.create(
        name="Инфраструктура", operation_type=operation_type
    )
    subcategory = SubCategory.objects.create(name="VPS", category=category)

    return {
        "status": status,
        "operation_type": operation_type,
        "category": category,
        "subcategory": subcategory,
    }


@pytest.fixture
def cashflow_record(references_data):
    return CashflowRecord.objects.create(
        record_date="2026-03-24",
        amount=Decimal("1500.00"),
        comment="Удаляемая запись",
        status=references_data["status"],
        operation_type=references_data["operation_type"],
        category=references_data["category"],
        subcategory=references_data["subcategory"],
    )


@pytest.mark.django_db
def test_cashflow_delete_page_returns_ok(client, cashflow_record):
    response = client.get(
        reverse(
            "transactions:cashflow_record_delete", kwargs={"pk": cashflow_record.pk}
        )
    )

    assert response.status_code == 200


@pytest.mark.django_db
def test_cashflow_delete_removes_record_and_redirects(client, cashflow_record):
    response = client.post(
        reverse(
            "transactions:cashflow_record_delete", kwargs={"pk": cashflow_record.pk}
        ),
        follow=True,
    )

    assert response.status_code == 200
    assert response.redirect_chain
    assert not CashflowRecord.objects.filter(pk=cashflow_record.pk).exists()

    messages = [m.message for m in get_messages(response.wsgi_request)]
    assert "Запись ДДС удалена." in messages


@pytest.mark.django_db
def test_cashflow_delete_get_returns_404_for_missing_record(client):
    response = client.get(
        reverse(
            "transactions:cashflow_record_delete",
            kwargs={"pk": "00000000-0000-0000-0000-000000000000"},
        )
    )

    assert response.status_code == 404


@pytest.mark.django_db
def test_cashflow_delete_post_returns_404_for_missing_record(client):
    response = client.post(
        reverse(
            "transactions:cashflow_record_delete",
            kwargs={"pk": "00000000-0000-0000-0000-000000000000"},
        )
    )

    assert response.status_code == 404
