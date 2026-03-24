from datetime import date, timedelta

import pytest
from django.urls import reverse

from apps.references.models.category import Category
from apps.references.models.operation_type import OperationType
from apps.references.models.status import Status
from apps.references.models.subcategory import SubCategory
from apps.transactions.models.cashflow_record import CashflowRecord


@pytest.fixture
def reference_data():
    """Создаёт минимальный набор справочников для тестов списка и фильтрации."""
    status_business = Status.objects.create(name="Бизнес")
    status_personal = Status.objects.create(name="Личное")

    operation_type = OperationType.objects.create(name="Списание")
    category = Category.objects.create(
        name="Инфраструктура",
        operation_type=operation_type,
    )
    subcategory = SubCategory.objects.create(
        name="VPS",
        category=category,
    )

    return {
        "status_business": status_business,
        "status_personal": status_personal,
        "operation_type": operation_type,
        "category": category,
        "subcategory": subcategory,
    }


@pytest.fixture
def cashflow_records_batch(reference_data):
    """Создаёт 100 записей ДДС для проверки пагинации и фильтрации."""
    records = []

    for i in range(100):
        status = (
            reference_data["status_business"]
            if i % 2 == 0
            else reference_data["status_personal"]
        )

        record = CashflowRecord.objects.create(
            record_date=date(2025, 1, 1) + timedelta(days=i),
            amount=1000 + i,
            comment=f"record {i}",
            status=status,
            operation_type=reference_data["operation_type"],
            category=reference_data["category"],
            subcategory=reference_data["subcategory"],
        )
        records.append(record)

    return records


@pytest.mark.django_db
def test_cashflow_list_first_page_contains_20_records(client, cashflow_records_batch):
    """
    Проверяет, что первая страница списка содержит 20 записей и пагинация включена.
    """
    response = client.get(reverse("home"))

    assert response.status_code == 200
    assert response.context["is_paginated"] is True
    assert response.context["page_obj"].number == 1
    assert len(response.context["cashflow_records"]) == 20


@pytest.mark.django_db
def test_cashflow_list_second_page_contains_20_records(client, cashflow_records_batch):
    """Проверяет, что на второй странице списка отображается 20 записей."""
    response = client.get(reverse("home"), {"page": 2})

    assert response.status_code == 200
    assert response.context["is_paginated"] is True
    assert response.context["page_obj"].number == 2
    assert len(response.context["cashflow_records"]) == 20


@pytest.mark.django_db
def test_cashflow_list_preserves_filter_on_second_page(
    client,
    reference_data,
    cashflow_records_batch,
):
    """Проверяет, что фильтр по статусу сохраняется при переходе на вторую страницу."""
    response = client.get(
        reverse("home"),
        {
            "status": str(reference_data["status_business"].id),
            "page": 2,
        },
    )

    assert response.status_code == 200
    assert response.context["is_paginated"] is True
    assert response.context["page_obj"].number == 2
    assert len(response.context["cashflow_records"]) == 20
    assert "status=" in response.context["querystring"]

    for record in response.context["cashflow_records"]:
        assert record.status_id == reference_data["status_business"].id


@pytest.mark.django_db
def test_cashflow_list_filters_by_date_range(client, cashflow_records_batch):
    """Проверяет фильтрацию списка по заданному диапазону дат."""
    response = client.get(
        reverse("home"),
        {
            "date_from": "2025-01-11",
            "date_to": "2025-01-20",
        },
    )

    assert response.status_code == 200
    assert len(response.context["cashflow_records"]) == 10

    for record in response.context["cashflow_records"]:
        assert date(2025, 1, 11) <= record.record_date <= date(2025, 1, 20)
