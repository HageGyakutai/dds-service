import uuid

from rest_framework.response import Response
from rest_framework.views import APIView


from apps.references.models.category import Category
from apps.references.models.subcategory import SubCategory


def _parse_uuid(value: str | None) -> uuid.UUID | None:
    """
    Преобразует строку в объект UUID.
    Если строка пустая, возвращает None.
    """
    if not value:
        return None
    try:
        return uuid.UUID(value)
    except (ValueError, TypeError):
        return None


class CategoriesByOperationTypeView(APIView):
    """
    Возвращает список категорий, относящихся к выбранному типу операции.

    Используется для динамической подгрузки категорий по operation_type_id
    в формах создания и редактирования записей.
    """

    def get(self, request, *args, **kwargs):
        """
        Обрабатывает GET-запрос и возвращает категории в формате JSON.
        """
        operation_type_id = _parse_uuid(request.GET.get("operation_type_id"))
        if not operation_type_id:
            return Response({"results": []})

        categories = Category.objects.filter(
            operation_type_id=operation_type_id
        ).order_by("name")

        data = [
            {"id": str(category.id), "name": category.name} for category in categories
        ]
        return Response({"results": data})


class SubCategoriesByCategoryView(APIView):
    """
    Возвращает список подкатегорий, относящихся к выбранной категории.

    Используется для динамической подгрузки подкатегорий по category_id
    в формах создания и редактирования записей.
    """

    def get(self, request, *args, **kwargs):
        """
        Обрабатывает GET-запрос и возвращает подкатегории в формате JSON.
        """
        category_id = _parse_uuid(request.GET.get("category_id"))
        if not category_id:
            return Response({"results": []})

        subcategories = SubCategory.objects.filter(category_id=category_id).order_by(
            "name"
        )

        data = [
            {"id": str(subcategory.id), "name": subcategory.name}
            for subcategory in subcategories
        ]
        return Response({"results": data})
