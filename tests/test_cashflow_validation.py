from decimal import Decimal

import pytest
from django.core.exceptions import ValidationError

from apps.references.models.category import Category
from apps.references.models.operation_type import OperationType
from apps.references.models.status import Status
from apps.references.models.subcategory import SubCategory
from apps.transactions.forms import CashflowRecordForm
from apps.transactions.models.cashflow_record import CashflowRecord


@pytest.fixture
def references_data():
    """Создает минимальный набор справочников для тестов валидации записи ДДС."""
    status = Status.objects.create(name="Налог")

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
def test_cashflow_form_is_valid_with_consistent_relations(references_data):
    """Проверяет, что форма валидна при согласованных типе, категории и подкатегории."""
    form = CashflowRecordForm(
        data={
            "record_date": "2026-03-23",
            "amount": "1222.00",
            "comment": "Важный платеж",
            "status": str(references_data["status"].pk),
            "operation_type": str(references_data["expense_type"].pk),
            "category": str(references_data["infrastructure"].pk),
            "subcategory": str(references_data["proxy"].pk),
        }
    )

    assert form.is_valid()


@pytest.mark.django_db
def test_cashflow_form_rejects_category_from_wrong_operation_type(references_data):
    """Проверяет, что форма отклоняет категорию от другого типа операции."""
    form = CashflowRecordForm(
        data={
            "record_date": "2026-03-23",
            "amount": "1222.00",
            "comment": "",
            "status": str(references_data["status"].pk),
            "operation_type": str(references_data["income_type"].pk),
            "category": str(references_data["infrastructure"].pk),
            "subcategory": str(references_data["proxy"].pk),
        }
    )

    assert not form.is_valid()
    assert "category" in form.errors
    assert form.errors["category"]


@pytest.mark.django_db
def test_cashflow_form_rejects_subcategory_from_wrong_category(references_data):
    """Проверяет, что форма отклоняет подкатегорию из другой категории."""
    form = CashflowRecordForm(
        data={
            "record_date": "2026-03-23",
            "amount": "1222.00",
            "comment": "",
            "status": str(references_data["status"].pk),
            "operation_type": str(references_data["expense_type"].pk),
            "category": str(references_data["infrastructure"].pk),
            "subcategory": str(references_data["farpost"].pk),
        }
    )

    assert not form.is_valid()
    assert "subcategory" in form.errors
    assert form.errors["subcategory"]


@pytest.mark.django_db
def test_cashflow_form_requires_amount_type_category_and_subcategory(references_data):
    """Проверяет обязательность суммы, типа операции, категории и подкатегории."""
    form = CashflowRecordForm(
        data={
            "record_date": "2026-03-23",
            "comment": "",
            "status": str(references_data["status"].pk),
        }
    )

    assert not form.is_valid()
    assert "amount" in form.errors
    assert "operation_type" in form.errors
    assert "category" in form.errors
    assert "subcategory" in form.errors


@pytest.mark.django_db
def test_cashflow_model_rejects_inconsistent_relations(references_data):
    """Проверяет, что модельная валидация отклоняет несогласованные связи."""
    record = CashflowRecord(
        record_date="2026-03-23",
        amount=Decimal("100.00"),
        comment="",
        status=references_data["status"],
        operation_type=references_data["income_type"],
        category=references_data["infrastructure"],
        subcategory=references_data["proxy"],
    )

    with pytest.raises(ValidationError) as exc_info:
        record.full_clean()

    assert "category" in exc_info.value.message_dict
