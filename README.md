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

- создание записей ДДС с проверкой логических зависимостей между типом операции, категорией и подкатегорией;
- просмотр списка записей ДДС;
- управление справочниками (`Status`, `OperationType`, `Category`, `SubCategory`) через отдельный раздел `/references/`;
- серверная валидация обязательных полей и доменных бизнес-правил.

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

Раздел `/transactions/` содержит пользовательский flow для записей ДДС:
список записей и форму создания с серверной валидацией связей между
типом операции, категорией и подкатегорией.

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
│       ├── migrations/
│       ├── models/
│       │   └── cashflow_record.py
│       ├── views/              # список и создание записей ДДС
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
│   ├── base.html
│   └── home.html
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

- [Главная страница](http://localhost:8000/)
- [Healthcheck](http://localhost:8000/health/)
- [Справочники](http://localhost:8000/references/)
- [Статусы](http://localhost:8000/references/statuses/)
- [Типы операций](http://localhost:8000/references/operation-types/)
- [Категории](http://localhost:8000/references/categories/)
- [Подкатегории](http://localhost:8000/references/subcategories/)
- [Записи ДДС](http://localhost:8000/transactions/)
- [Создание записи ДДС](http://localhost:8000/transactions/create/)
- [Django Admin](http://localhost:8000/admin/)

---

## Тестирование

```bash
uv run pytest
```
Ключевые проверки валидации записи ДДС находятся в `tests/test_cashflow_validation.py`.


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
