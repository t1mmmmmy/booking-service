# Booking Service

HTTP JSON API для управления номерами отеля и бронированиями.

Сервис позволяет создавать и удалять номера, получать их список с сортировкой, создавать и удалять бронирования, получать брони конкретного номера.

Авторизация не требуется.

## Технологии

- Python 3.13+
- Django и Django REST Framework
- PostgreSQL 18
- uv
- Docker и Docker Compose
- pydantic-settings
- Ruff, mypy и pre-commit

## Запуск

Для запуска приложения нужны Git, Docker и Docker Compose.

### 1. Клонировать репозиторий

На этапе разработки код находится в ветке `dev`:

```powershell
git clone --branch dev https://github.com/t1mmmmmy/booking-service.git
cd booking-service
```

### 2. Подготовить конфигурацию

Скопировать шаблон:

```powershell
Copy-Item .env.example .env
```

Заполнить `.env` собственными значениями. Пример локальной конфигурации:

```dotenv
SECRET_KEY=replace-with-your-random-secret-key
DEBUG=true
ALLOWED_HOSTS=["localhost","127.0.0.1"]

DB_NAME=booking
DB_USER=booking_user
DB_PASSWORD=replace-with-your-database-password
DB_HOST=127.0.0.1
DB_PORT=5432
```

`SECRET_KEY` и `DB_PASSWORD` нужно заменить своими значениями.

`ALLOWED_HOSTS` задаётся JSON-массивом строк. Внутри контейнера приложения `DB_HOST` автоматически переопределяется на `postgres` — имя сервиса базы данных в Compose.

Файл `.env` исключён из Git.

### 3. Запустить сервисы

```powershell
docker compose up -d --build
```

При запуске приложение дожидается готовности PostgreSQL, применяет неприменённые миграции и запускает сервер.

Посмотреть логи:

```powershell
docker compose logs -f web
```

После запуска API доступно по адресу:

```text
http://localhost:8000
```

Проверка доступности:

```powershell
curl.exe http://localhost:8000/ping/
```

Ответ:

```json
{"status": 200}
```

Команды ниже используют `curl.exe`, поскольку в Windows PowerShell имя `curl` может быть псевдонимом `Invoke-WebRequest`.

## Управление контейнерами

Состояние сервисов:

```powershell
docker compose ps
```

Логи приложения и базы:

```powershell
docker compose logs -f
```

Остановка с удалением контейнеров:

```powershell
docker compose down
```

Данные PostgreSQL сохраняются в именованном volume `postgres_data`. Обычная команда `docker compose down` его не удаляет.

После изменения зависимостей можно пересобрать приложение и обновить его виртуальное окружение:

```powershell
docker compose up -d --build --force-recreate --renew-anon-volumes web
```

## API

Маршруты используются без завершающего `/`.

| Метод | Маршрут | Назначение |
|---|---|---|
| POST | `/rooms/create` | Создать номер |
| GET | `/rooms/list` | Получить список номеров |
| DELETE | `/rooms/delete/{id}` | Удалить номер и его брони |
| POST | `/bookings/create` | Создать бронь |
| GET | `/bookings/list` | Получить список броней |
| DELETE | `/bookings/delete/{id}` | Удалить бронь |

POST-запросы поддерживают JSON и данные HTML-формы. В примерах используется форма.

ID в примерах условные: подставляйте значения, полученные при создании объектов.

### Создание номера

Обязательные поля:

- `description` — текстовое описание;
- `price` — положительная цена за ночь, до двух знаков после запятой.

```powershell
curl.exe -i -X POST --data-urlencode "description=Номер с видом на океан" -d "price=199.99" http://localhost:8000/rooms/create
```

Статус: `201 Created`.

```json
{"room_id": 1}
```

### Список номеров

```powershell
curl.exe "http://localhost:8000/rooms/list"
```

Пример ответа:

```json
[
  {
    "id": 1,
    "price": "199.99",
    "description": "Номер с видом на океан",
    "added_at": "2026-11-03T12:00:00Z"
  }
]
```

Сортировка задаётся параметром `ordering`:

| Значение | Порядок |
|---|---|
| `price` | По цене, по возрастанию |
| `-price` | По цене, по убыванию |
| `added_at` | По дате добавления, от старых к новым |
| `-added_at` | По дате добавления, от новых к старым |

Пример:

```powershell
curl.exe "http://localhost:8000/rooms/list?ordering=-price"
```

Без параметра `ordering` порядок номеров не гарантируется.

### Создание брони

Обязательные поля:

- `room` — ID существующего номера;
- `date_start` — дата начала;
- `date_end` — дата окончания.

Для передачи дат используйте формат `YYYY-MM-DD`. Дата начала должна быть раньше даты окончания.

```powershell
curl.exe -i -X POST -d "room=1" -d "date_start=2026-12-10" -d "date_end=2026-12-15" http://localhost:8000/bookings/create
```

Статус: `201 Created`.

```json
{"booking_id": 1}
```

### Список броней номера

```powershell
curl.exe "http://localhost:8000/bookings/list?room_id=1"
```

Пример ответа:

```json
[
  {
    "id": 1,
    "date_start": "2026-12-10",
    "date_end": "2026-12-15",
    "room": 1
  }
]
```

Брони сортируются по дате начала по возрастанию.

Если `room_id` не передан, возвращается список всех броней. Если у указанного номера нет броней, возвращается пустой массив.

### Удаление брони

```powershell
curl.exe -i -X DELETE http://localhost:8000/bookings/delete/1
```

При успешном удалении возвращается `204 No Content` без тела ответа. Номер при этом сохраняется.

### Удаление номера

```powershell
curl.exe -i -X DELETE http://localhost:8000/rooms/delete/1
```

При успешном удалении возвращается `204 No Content` без тела ответа.

Все брони удаляемого номера также удаляются.

## Ошибки

Ошибки валидации возвращаются в JSON со статусом `400 Bad Request`.

Например, для нулевой или отрицательной цены:

```json
{
  "price": [
    "Цена должна быть положительной"
  ]
}
```

Для одинаковых или перепутанных дат:

```json
{
  "non_field_errors": [
    "Дата начала должна быть раньше даты конца бронирования"
  ]
}
```

Попытка удалить несуществующий объект возвращает `404 Not Found` с описанием ошибки в JSON.

## Миграции

Для управления схемой БД используются Django-миграции, сохранённые в репозитории.

При старте контейнера приложения они применяются автоматически. Применить их вручную:

```powershell
docker compose exec web python src/manage.py migrate
```

После изменения моделей создать новую миграцию:

```powershell
docker compose exec web python src/manage.py makemigrations catalog
```

Файлы миграций необходимо добавлять в Git вместе с изменениями моделей.

## Проверки кода

Для локальных проверок нужны Python 3.13+ и uv. Для команды `make check` дополнительно требуется GNU Make.

Установить зависимости разработки:

```powershell
uv sync --locked
```

Запустить проверки:

```powershell
make check
```

Команда запускает Ruff, форматтер и mypy. Ruff и форматтер автоматически изменяют файлы, поэтому после выполнения следует просмотреть `git diff`.

Запустить проверки без автоматического исправления исходников можно отдельно:

```powershell
uv run ruff check src
uv run ruff format --check src
uv run mypy src
```

Установить Git hook:

```powershell
uv run pre-commit install
```

После установки проверки будут запускаться перед коммитом.

## Автоматические тесты

На текущем этапе автоматические тесты ещё не добавлены. Планируется покрытие API с помощью pytest и pytest-django.

## Принятые решения

- Для схемы БД используются Django-миграции вместо отдельного SQL-файла.
- При создании брони ID номера передаётся в поле `room`; при фильтрации списка — в параметре `room_id`.
- Создание возвращает `room_id` или `booking_id`. В списках идентификатор объекта называется `id`.
- Цена должна быть строго положительной.
- Дата окончания брони должна быть позже даты начала. Бронирование с одинаковыми датами запрещено.
- Применяется стандартный разбор дат DRF; в документации используется формат `YYYY-MM-DD`.
- Проверка пересечения броней не реализована: по базовому ТЗ она необязательна.
- Удаление возвращает `204 No Content` без JSON-тела.
- Docker Compose настроен для локальной разработки с Django `runserver`.