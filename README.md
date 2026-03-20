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

- `transactions` — работа с денежными операциями (ДДС)

- `references` — справочники и классификаторы

Связи моделей:
```text
Transaction
 ├── status → Status
 ├── type → TransactionType
 ├── category → Category
 └── subcategory → SubCategory

Category → TransactionType
SubCategory → Category
```

---

## Структура проекта

```text
.
├── apps/
│   ├── references/        # справочники (статусы, типы, категории, подкатегории)
│   │   ├── management/    # кастомные команды (создание суперпользователя)
│   │   ├── models.py
│   │   ├── admin.py
│   │   └── views.py
│   │
│   └── transactions/      # операции ДДС (основная бизнес-логика)
│       ├── models.py
│       ├── admin.py
│       └── views.py
│
├── config/                # конфигурация Django
│   ├── settings/
│   │   ├── base.py
│   │   └── components/    # разбитые настройки (database, middleware, и т.д.)
│   ├── urls.py
│   └── wsgi.py
│
├── docs/                  # документация и материалы задания
├── locale/                # переводы (i18n)
├── logs/                  # логи приложения
├── tests/                 # тесты
│
├── Dockerfile
├── docker-compose.yml
├── entrypoint.sh          # инициализация контейнера (миграции, суперпользователь)
├── manage.py
└── pyproject.toml
```
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
uv run black --check .
uv run flake8 .
uv run mypy .
uv run pytest --maxfail=1 --disable-warnings
```
