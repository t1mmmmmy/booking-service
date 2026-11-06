# Booking Service

JSON API для управления номерами отеля и бронированиями без авторизации.

Python 3.13+, Django REST Framework, PostgreSQL 18, uv, Docker Compose, pydantic-settings, Loguru.

## Запуск

Нужны Git и запущенный Docker с Docker Compose. Команды для PowerShell:

```powershell
git clone --branch dev https://github.com/t1mmmmmy/booking-service.git
cd booking-service
Copy-Item .env.example .env
```

Заполните `.env` своими значениями:

```dotenv
SECRET_KEY=replace-with-your-random-secret-key
DEBUG=true
ALLOWED_HOSTS=["localhost","127.0.0.1"]
DB_NAME=booking
DB_USER=booking
DB_PASSWORD=replace-with-your-password
DB_HOST=postgres
DB_PORT=5432
```

```powershell
docker compose up -d --build
```

API: http://localhost:8000. Миграции применяются автоматически. Данные сохраняются в Docker volume после `docker compose down`. Файл `.env` исключён из Git.

## API

| Метод | Путь | Назначение / параметры |
|---|---|---|
| GET | `/ping/` | Проверка доступности |
| POST | `/rooms/create` | Создать номер: `description`, `price` → `room_id` |
| GET | `/rooms/list` | Список номеров; `ordering=price`, `-price`, `added_at`, `-added_at` |
| DELETE | `/rooms/delete/{id}` | Удалить номер и его брони |
| POST | `/bookings/create` | Создать бронь: `room`, `date_start`, `date_end` → `booking_id` |
| GET | `/bookings/list?room_id={id}` | Брони номера по дате начала; без фильтра — все брони |
| DELETE | `/bookings/delete/{id}` | Удалить бронь |

Цена должна быть положительной. Даты — `YYYY-MM-DD`, начало раньше окончания. Пересечения броней не проверяются. Создание возвращает `201`, удаление — `204` без тела, ошибки — JSON.

Пример создания номера в PowerShell:

```powershell
curl.exe -X POST --data-urlencode "description=Номер с видом на океан" -d "price=199.99" http://localhost:8000/rooms/create
```

## Проверки и логи

- `make check` — Ruff (с исправлениями и форматированием) и mypy; нужны uv и Make.
- `make test` — запуск контейнеров и pytest в отдельной временной тестовой БД; нужен Make.
- `docker compose logs -f web` — логи приложения, включая создание и удаление номеров и броней через Loguru.
- `docker compose down` — остановка и удаление контейнеров с сохранением данных БД.
