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

- CRUD для записей ДДС;
- фильтрация по дате, статусу, типу, категории и подкатегории;
- CRUD для справочников (статусы, типы, категории, подкатегории);
- валидация бизнес-правил на сервере и клиенте.

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

- API: http://localhost:8000/
- Admin: http://localhost:8000/admin/

---

## Архитектура проекта

Проект разделен на два основных домена:

- `transactions` — работа с денежными операциями ДДС
- `references` — справочники и классификаторы

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
│   ├── references/            # справочники: статусы, типы, категории, подкатегории
│   │   ├── data/               # seed-данные справочников
│   │   ├── management/
│   │   │   └── commands/      # кастомные management-команды
│   │   │       ├── createsuperuser_if_none_exists.py  
│   │   │       └── seed_references.py     
│   │   ├── migrations/
│   │   ├── models/
│   │   │   ├── mixins.py
│   │   │   ├── status.py
│   │   │   ├── operation_type.py
│   │   │   ├── category.py
│   │   │   └── subcategory.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── tests.py
│   │   └── views.py
│   │
│   └── transactions/           # денежные операции ДДС
│       ├── migrations/
│       ├── models/
│       │   └── cashflow_record.py
│       ├── admin.py
│       ├── apps.py
│       ├── tests.py
│       └── views.py
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
├── templates/                  # базовые HTML-шаблоны
├── tests/                      # smoke-тесты проекта
│
├── Dockerfile
├── docker-compose.yml
├── entrypoint.sh
├── manage.py
├── pyproject.toml
└── README.md
```
- `createsuperuser_if_none_exists.py` — автосоздание суперпользователя
- `seed_references.py` — заполнение стартовых справочников
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

---

## Миграции и заполнение справочников
```bash
uv run python manage.py migrate
uv run python manage.py seed_references
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


## Документация API

В разработке.

---

## Основные эндпоинты

В разработке.

---

## Тестирование

```bash
uv run pytest
```

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
