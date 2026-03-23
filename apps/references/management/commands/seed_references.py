from django.core.management.base import BaseCommand
from django.db import transaction

from apps.references.data.seed_data import STATUSES, OPERATION_TYPES, CATEGORY_TREE
from apps.references.models.status import Status
from apps.references.models.operation_type import OperationType
from apps.references.models.category import Category
from apps.references.models.subcategory import SubCategory


class Command(BaseCommand):
    """
    Django management-команда для начального заполнения справочников.

    Создаёт базовые данные для работы приложения:
    - статусы (Status)
    - типы операций (OperationType)
    - категории (Category)
    - подкатегории (SubCategory)

    Команда идемпотентна: при повторном запуске не создаёт дубликаты,
    так как использует get_or_create.
    """

    help = "Seed reference data for DDS service"

    @transaction.atomic
    def handle(self, *args, **options):
        """
        Последовательно запускает заполнение:
        1. Статусов
        2. Типов операций
        3. Категорий и подкатегорий

        Вся операция обёрнута в транзакцию: при возникновении ошибки
        изменения не будут частично применены.

        Выводит краткую статистику по созданным объектам.
        """
        created_statuses = self.seed_statuses()
        created_operation_types = self.seed_operation_types()
        created_categories, created_subcategories = (
            self.seed_categories_and_subcategories()
        )

        self.stdout.write(self.style.SUCCESS("Reference data seeding completed."))
        self.stdout.write(f"Statuses created: {created_statuses}")
        self.stdout.write(f"Operation types created: {created_operation_types}")
        self.stdout.write(f"Categories created: {created_categories}")
        self.stdout.write(f"Subcategories created: {created_subcategories}")

    def seed_statuses(self) -> int:
        """
        Создает базовые статусы из списка STATUSES.
        """
        created_count = 0

        for name in STATUSES:
            _, created = Status.objects.get_or_create(name=name)
            if created:
                created_count += 1

        return created_count

    def seed_operation_types(self) -> int:
        """
        Создает базовые типы операций из списка OPERATION_TYPES.
        """
        created_count = 0

        for name in OPERATION_TYPES:
            _, created = OperationType.objects.get_or_create(name=name)
            if created:
                created_count += 1
        return created_count

    def seed_categories_and_subcategories(self) -> tuple[int, int]:
        """
        Создаёт категории и подкатегории на основе структуры CATEGORY_TREE
        Логика:
        - каждая категория привязывается к типу операции (OperationType)
        - каждая подкатегория привязывается к категории (Category)
        """
        created_categories = 0
        created_subcategories = 0

        for operation_type_data in CATEGORY_TREE:
            operation_type = OperationType.objects.get(
                name=operation_type_data["operation_type"],
            )

            for category_data in operation_type_data["categories"]:
                category, category_created = Category.objects.get_or_create(
                    name=category_data["name"],
                    operation_type=operation_type,
                )

                if category_created:
                    created_categories += 1

                for subcategory_name in category_data["subcategories"]:
                    _, subcategory_created = SubCategory.objects.get_or_create(
                        name=subcategory_name,
                        category=category,
                    )
                    if subcategory_created:
                        created_subcategories += 1

        return created_categories, created_subcategories
