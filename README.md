# dds-service

## Назначение

Тестовое задание для позиции backend-разработчик.

Веб-приложение для учета движения денежных средств (ДДС): создание, просмотр, редактирование,
удаление и фильтрация операций.

---

## Описание проекта
Сервис помогает вести учет финансовых операций с учетом логических зависимостей:

- категория принадлежит типу операции;
- подкатегория принадлежит категории.

---

## Основные возможности

- создание и редактирование записей ДДС с проверкой логических зависимостей между типом операции, категорией и подкатегорией;
- динамические зависимости на форме записи: категории фильтруются по типу операции, подкатегории — по категории;
- просмотр списка записей ДДС на главной странице;
- фильтрация записей ДДС по периоду дат, статусу, типу операции, категории и подкатегории;
- управление справочниками (`Status`, `OperationType`, `Category`, `SubCategory`) через отдельный раздел `/references/`;
- серверная валидация обязательных полей и доменных бизнес-правил.
- удаление записи ДДС через отдельную страницу подтверждения, с редиректом на список и сообщением об успешном удалении;

---

## Динамические зависимости формы

Для формы создания/редактирования записи ДДС реализованы зависимые поля:

- `operation_type` -> список `category`
- `category` -> список `subcategory`

Технически:

- backend: DRF API endpoints в `apps/transactions/views/dependencies.py`;
- frontend: JS-логика в `apps/transactions/static/transactions/form_dependencies.js`;
- серверная защита: ограничение queryset в `CashflowRecordForm.__init__` + валидация в `clean()`.

---

## Удаление записи ДДС

Реализован отдельный сценарий удаления записи ДДС:

- ссылка `Удалить` доступна в таблице списка записей;
- перед удалением показывается страница подтверждения действия;
- удаление выполняется `POST`-запросом с CSRF-защитой;
- после успешного удаления пользователь возвращается к списку записей и видит сообщение об успехе;
- для несуществующей записи возвращается корректный `404`;

---

## Технологический стек

- Python 3.13
- Django
- Django ORM
- Django REST Framework
- PostgreSQL
- Docker / Docker Compose
- uv, pre-commit, GitHub Actions

---

## Быстрый старт

```bash
docker compose up -d --build
```

После запуска сервис будет доступен:

- Web: http://localhost:8000/
- Admin: http://localhost:8000/admin/

---

## Архитектура проекта

Проект разделен на два основных домена:

- `transactions` — работа с денежными операциями ДДС
- `references` — справочники и классификаторы

Раздел `/references/` предназначен для управления справочниками.
В нём доступны списки и CRUD для `Status`, `OperationType`, `Category` и `SubCategory`.

Главная страница `/` отображает список записей ДДС с фильтрацией и пагинацией.

Раздел `/transactions/` содержит пользовательский flow для записей ДДС:
формы создания и редактирования записи, а также routes, связанные с операциями ДДС.

Связи моделей:

```text
CashflowRecord
 ├── status → Status
 ├── operation_type → OperationType
 ├── category → Category
 └── subcategory → SubCategory

Category → OperationType
SubCategory → Category
```

---

## Структура проекта

```text
.
├── apps/
│   ├── references/             # справочники: статусы, типы, категории, подкатегории
│   │   ├── data/               # seed-данные справочников
│   │   ├── management/
│   │   │   └── commands/       # кастомные management-команды
│   │   ├── migrations/
│   │   ├── models/
│   │   │   ├── mixins.py
│   │   │   ├── status.py
│   │   │   ├── operation_type.py
│   │   │   ├── category.py
│   │   │   └── subcategory.py
│   │   ├── views/              # CRUD-views раздела справочников
│   │   ├── forms.py            # формы для управления справочниками
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── tests.py
│   │   └── urls.py
│   │
│   └── transactions/           # денежные операции ДДС
│       ├── management/
│       │   └── commands/       # management-команды для записей ДДС
│       ├── migrations/
│       ├── models/
│       │   └── cashflow_record.py
│       ├── views/              # список, создание и редактирование записей ДДС
│       ├── filters.py          # фильтрация списка записей ДДС
│       ├── forms.py            # формы и валидация записей ДДС
│       ├── admin.py
│       ├── apps.py
│       ├── tests.py
│       └── urls.py
│
├── config/                     # конфигурация Django-проекта
│   ├── settings/
│   │   ├── components/         # database, middleware, templates, static, etc.
│   │   └── base.py
│   ├── urls.py
│   ├── views.py
│   ├── asgi.py
│   └── wsgi.py
│
├── templates/
│   ├── references/             # шаблоны раздела справочников
│   ├── transactions/           # шаблоны списка и формы записей ДДС
│   └── base.html
│
├── tests/                      # тесты проекта
├── Dockerfile
├── docker-compose.yml
├── entrypoint.sh
├── manage.py
├── pyproject.toml
└── README.md
```
- `createsuperuser_if_none_exists.py` — автосоздание суперпользователя
- `seed_references.py` — заполнение стартовых справочников
- `seed_cashflow_records.py` — генерация тестовых записей ДДС для ручной проверки фильтров и пагинации

---

## Запуск проекта

Клонировать репозиторий
```bash
git clone https://github.com/HageGyakutai/dds-service.git
cd dds-service
```
Подготовить переменные окружения:
 ```bash
 cp .env.example .env
 ```
Запуск через Docker
```bash
docker compose up -d --build
```
> При старте контейнера автоматически применяются миграции, выполняется заполнение стартовых справочников и проверяется наличие суперпользователя.

Для ручной проверки списка, фильтров и пагинации можно сгенерировать тестовые записи.
По умолчанию команда создаёт `100` записей:

```bash
docker compose exec web uv run python manage.py seed_cashflow_records
```
Дополнительные параметры:
- `--count` — количество записей
- `--start-date` — дата начала генерации в формате YYYY-MM-DD

---

## Миграции и заполнение справочников
```bash
uv run python manage.py migrate
uv run python manage.py seed_references
uv run python manage.py seed_cashflow_records
```

---

## Доступ к админ-панели
Админ-панель доступна по адресу:

http://localhost:8000/admin/

Суперпользователь создается автоматически при запуске контейнера
через кастомную Django management-команду:
```bash
uv run python manage.py createsuperuser_if_none_exists
```
Данные берутся из переменных окружения `.env`.

### Данные по умолчанию

```text
Username: admin
Email: admin@example.com
Password: admin
```
### Настройка

Вы можете изменить данные суперпользователя в `.env`:
```dotenv
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_PASSWORD=admin
```
> Рекомендуется изменить пароль перед использованием.

---

## Основные эндпоинты

- [Главная страница / список записей ДДС](http://localhost:8000/)
- [Healthcheck](http://localhost:8000/health/)
- [Справочники](http://localhost:8000/references/)
- [Статусы](http://localhost:8000/references/statuses/)
- [Типы операций](http://localhost:8000/references/operation-types/)
- [Категории](http://localhost:8000/references/categories/)
- [Подкатегории](http://localhost:8000/references/subcategories/)
- [Список записей ДДС](http://localhost:8000/transactions/)
- [Создание записи ДДС](http://localhost:8000/transactions/create/)
- `GET /transactions/api/categories/?operation_type_id=<uuid>` — категории по типу операции
- `GET /transactions/api/subcategories/?category_id=<uuid>` — подкатегории по категории
- `GET /transactions/<uuid:pk>/delete/` — страница подтверждения удаления записи ДДС
- `POST /transactions/<uuid:pk>/delete/` — подтверждение и удаление записи ДДС
- [Django Admin](http://localhost:8000/admin/)

---

## Тестирование

Основной способ запуска тестов в проекте — внутри контейнера.

Установка `dev`-зависимостей в уже поднятый контейнер:

```bash
docker compose exec web uv sync --extra dev
```

Запуск тестов:

```bash
docker compose exec web uv run pytest
```

Ключевые сценарии покрыты отдельными тестовыми файлами:
- `tests/test_cashflow_validation.py` — серверная валидация записи ДДС;
- `tests/test_cashflow_list_filtering.py` — список, фильтрация и пагинация;
  - включает кейс фильтрации по диапазону дат (`date_from`/`date_to`);
- `tests/test_cashflow_create.py` — создание записи ДДС (GET формы, успешный create, невалидные сценарии по доменным связям);
- `tests/test_cashflow_update.py` — редактирование записи ДДС;
- `tests/test_cashflow_dynamic_dependencies.py` — API и динамические зависимости полей формы;
- `tests/test_cashflow_delete.py` — удаление записи ДДС (confirm page, успешное удаление, 404 для несуществующей записи).
---

## Автор

Запольских Сергей

https://github.com/HageGyakutai

---

## Локальные проверки

```bash
uv run pre-commit install
uv run pre-commit run --all-files
```

```bash
uv sync --extra dev
uv run black --check .
uv run flake8 .
uv run mypy .
uv run pytest --maxfail=1 --disable-warnings
```
