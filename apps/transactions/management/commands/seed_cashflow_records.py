from datetime import date, timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from apps.references.models.category import Category
from apps.references.models.status import Status
from apps.transactions.models.cashflow_record import CashflowRecord


class Command(BaseCommand):
    """Создает тестовый набор записей ДДС для ручной проверки интерфейса."""

    help = "Seed test cashflow records for manual UI checks"

    def add_arguments(self, parser):
        parser.add_argument(
            "--count",
            type=int,
            default=100,
            help="Количество записей для генерации",
        )
        parser.add_argument(
            "--start-date",
            type=date.fromisoformat,
            default=date(2025, 1, 1),
            help="Дата начала генерации в формате YYYY-MM-DD",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        """Проверяет справочники и создает указанное количество записей."""
        count = options["count"]
        start_date = options["start_date"]

        if count <= 0:
            raise CommandError("Параметр --count должен быть положительным числом.")

        statuses = list(Status.objects.order_by("name"))
        categories = list(
            Category.objects.select_related("operation_type").order_by("name")
        )

        if not statuses:
            raise CommandError(
                "Нет статусов. Сначала выполни: python manage.py seed_references",
            )

        if not categories:
            raise CommandError(
                "Нет категорий. Сначала выполни: python manage.py seed_references",
            )

        created_records = 0

        for index in range(count):
            category = categories[index % len(categories)]
            subcategories = list(category.subcategories.order_by("name"))

            if not subcategories:
                raise CommandError(
                    f"У категории '{category.name}' нет подкатегорий.",
                )

            status = statuses[index % len(statuses)]
            subcategory = subcategories[index % len(subcategories)]

            CashflowRecord.objects.create(
                record_date=start_date + timedelta(days=index % 60),
                amount=Decimal("1000.00") + Decimal(index * 125),
                comment=f"Тестовая запись #{index + 1}",
                status=status,
                operation_type=category.operation_type,
                category=category,
                subcategory=subcategory,
            )
            created_records += 1

        self.stdout.write(self.style.SUCCESS("Тестовые записи ДДС успешно созданы."))
        self.stdout.write(f"Создано записей: {created_records}")
