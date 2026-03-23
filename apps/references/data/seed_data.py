from typing import TypedDict


class CategorySeedItem(TypedDict):
    name: str
    subcategories: list[str]


class OperationTypeSeedItem(TypedDict):
    operation_type: str
    categories: list[CategorySeedItem]


STATUSES: list[str] = [
    "Бизнес",
    "Личное",
    "Налог",
]

OPERATION_TYPES: list[str] = [
    "Пополнение",
    "Списание",
]

CATEGORY_TREE: list[OperationTypeSeedItem] = [
    {
        "operation_type": "Списание",
        "categories": [
            {
                "name": "Инфраструктура",
                "subcategories": ["VPS", "Proxy"],
            },
            {
                "name": "Маркетинг",
                "subcategories": ["Farpost", "Avito"],
            },
        ],
    },
    {
        "operation_type": "Пополнение",
        "categories": [],
    },
]
