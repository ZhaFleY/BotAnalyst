# Архитектура (DDD)

Проект разделён на два приложения:

- `bot/` — Telegram-бот (aiogram)
- `backend/` — API (FastAPI) + фоновые задачи (Celery)

## Backend

DDD-структура построена вокруг bounded contexts в `backend/modules/`:

- `backend/modules/files/` — приём/хранение файлов и запуск обработки
  - `application/` — оркестрация (workflow)
  - `presentation/http/` — FastAPI роутеры
  - `presentation/celery/` — Celery-задачи (delivery)
  - `infrastructure/` — адаптеры (MinIO и т.п.)
- `backend/modules/analysis/` — аналитика/LLM и форматирование ответа
  - `application/` — use-cases (forecast, formatter)
  - `infrastructure/llm/` — конкретный провайдер/инструменты

Shared kernel:

- `backend/shared/` — общие утилиты (zip-распаковка, Telegram client, логирование)

Entry points (тонкие файлы, которые запускаются из docker-compose):

- `backend/app.py` → `backend/entrypoints/fastapi_app.py`
- `backend/celery_app.py` → `backend/entrypoints/celery_worker.py`

Слои `backend/application/*`, `backend/presentation/*`, `backend/infrastructure/*`, `backend/utils/*`, `backend/ai/*` оставлены как совместимые “фасады” (wrappers) и перекидывают импорты на `backend/modules/*`/`backend/shared/*`.

## Bot

- `bot/presentation/telegram/*` — роутеры/клавиатуры/FSM (delivery слой)
- `bot/shared/*` — общие мелкие утилиты
- `bot/entrypoints/telegram_bot.py` — точка входа, `app.py` остаётся стабильным wrapper’ом для запуска

