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
    """Создаёт минимальный набор справочников для тестов редактирования записи ДДС."""
    status_business = Status.objects.create(name="Бизнес")
    status_personal = Status.objects.create(name="Личное")

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
    vps = SubCategory.objects.create(name="VPS", category=infrastructure)
    farpost = SubCategory.objects.create(name="Farpost", category=marketing)

    return {
        "status_business": status_business,
        "status_personal": status_personal,
        "income_type": income_type,
        "expense_type": expense_type,
        "infrastructure": infrastructure,
        "marketing": marketing,
        "proxy": proxy,
        "vps": vps,
        "farpost": farpost,
    }


@pytest.fixture
def cashflow_record(references_data):
    """Создаёт запись ДДС для сценариев редактирования."""
    return CashflowRecord.objects.create(
        record_date="2026-03-23",
        amount=Decimal("1200.00"),
        comment="Исходная запись",
        status=references_data["status_business"],
        operation_type=references_data["expense_type"],
        category=references_data["infrastructure"],
        subcategory=references_data["proxy"],
    )


@pytest.mark.django_db
def test_cashflow_update_page_returns_ok(client, cashflow_record):
    """Проверяет, что страница редактирования существующей записи открывается."""
    response = client.get(
        reverse(
            "transactions:cashflow_record_update",
            kwargs={"pk": cashflow_record.pk},
        )
    )

    assert response.status_code == 200


@pytest.mark.django_db
def test_cashflow_update_saves_valid_changes(client, references_data, cashflow_record):
    """Проверяет, что валидное редактирование сохраняет изменения записи."""
    response = client.post(
        reverse(
            "transactions:cashflow_record_update",
            kwargs={"pk": cashflow_record.pk},
        ),
        data={
            "record_date": "2026-03-24",
            "amount": "2500.00",
            "comment": "Обновлённая запись",
            "status": str(references_data["status_personal"].pk),
            "operation_type": str(references_data["expense_type"].pk),
            "category": str(references_data["infrastructure"].pk),
            "subcategory": str(references_data["vps"].pk),
        },
    )

    cashflow_record.refresh_from_db()

    assert response.status_code == 302
    assert cashflow_record.record_date.isoformat() == "2026-03-24"
    assert cashflow_record.amount == Decimal("2500.00")
    assert cashflow_record.comment == "Обновлённая запись"
    assert cashflow_record.status_id == references_data["status_personal"].id
    assert cashflow_record.subcategory_id == references_data["vps"].id


@pytest.mark.django_db
def test_cashflow_update_rejects_category_from_wrong_operation_type(
    client,
    references_data,
    cashflow_record,
):
    """Проверяет, что редактирование отклоняет категорию от другого типа операции."""
    response = client.post(
        reverse(
            "transactions:cashflow_record_update",
            kwargs={"pk": cashflow_record.pk},
        ),
        data={
            "record_date": "2026-03-23",
            "amount": "1200.00",
            "comment": "Невалидное обновление",
            "status": str(references_data["status_business"].pk),
            "operation_type": str(references_data["income_type"].pk),
            "category": str(references_data["infrastructure"].pk),
            "subcategory": str(references_data["proxy"].pk),
        },
    )

    cashflow_record.refresh_from_db()

    assert response.status_code == 200
    assert "category" in response.context["form"].errors
    assert (
        response.context["form"].errors["category"][0]
        == "Выбранная категория не относится к указанному типу операции."
    )
    assert cashflow_record.operation_type_id == references_data["expense_type"].id


@pytest.mark.django_db
def test_cashflow_update_rejects_subcategory_from_wrong_category(
    client,
    references_data,
    cashflow_record,
):
    """Проверяет, что редактирование отклоняет подкатегорию из другой категории."""
    response = client.post(
        reverse(
            "transactions:cashflow_record_update",
            kwargs={"pk": cashflow_record.pk},
        ),
        data={
            "record_date": "2026-03-23",
            "amount": "1200.00",
            "comment": "Невалидное обновление",
            "status": str(references_data["status_business"].pk),
            "operation_type": str(references_data["expense_type"].pk),
            "category": str(references_data["infrastructure"].pk),
            "subcategory": str(references_data["farpost"].pk),
        },
    )

    cashflow_record.refresh_from_db()

    assert response.status_code == 200
    assert "subcategory" in response.context["form"].errors
    assert (
        response.context["form"].errors["subcategory"][0]
        == "Выбранная подкатегория не относится к указанной категории."
    )
    assert cashflow_record.subcategory_id == references_data["proxy"].id
