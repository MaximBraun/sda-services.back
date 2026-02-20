# sda-services.back

Мультисервисный backend на `FastAPI` для генерации медиа и AI-сценариев (Pixverse, ChatGPT, Pika, Wan, Qwen и др.).

## Стек

- Python 3.11
- FastAPI / Pydantic
- Uvicorn
- Docker / Docker Compose
- Celery (воркеры)
- Redis / RabbitMQ / PostgreSQL / ClickHouse (через DSN в `.env`)

## Структура запуска

Каждый сервис запускается отдельным контейнером с `APP_SERVICE`, например:
- `auth`, `pixverse`, `chatgpt`, `dashboard`, `calories`, `instagram`, `cosmetic`, `qwen`, `topmedia`, `user`, `gamestone`, `shark`, `pika`, `wan`, `cheaterbuster`, `ximilar`

API внутри сервиса имеет префикс `api_prefix` (по умолчанию `/api/v1`).

## Быстрый старт (Docker)

1. Создать `.env` на основе `.env.example`.
2. Заполнить обязательные переменные окружения.
3. Запустить контейнеры:

```bash
docker compose up -d --build
```

Если меняли код и/или `.env`, рекомендуется:

```bash
docker compose up -d --build --force-recreate
```

Проверка:

```bash
docker compose ps
docker compose logs -f pixverse
```

## Запуск отдельного сервиса

```bash
docker compose up -d --build pixverse
```

## Переменные окружения

Минимально нужны (см. `.env.example`):

- `APP_ENV`
- `APP_PORT`
- `APP_HOST`
- `CLICKHOUSE_DSN_URL`
- `DATABASE_DSN_URL`
- `RABBITMQ_DSN_URL`
- `REDIS_DSN_URL`
- `SECRET_KEY`
- `ALGORITHM`
- `DOMAIN_URL`
- `CHATGPT_TOKEN`
- `ROCKET_TOKEN`
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`

Опционально для отдачи статики отдельным URL:

- `STATIC_BASE_URL` (если используется в вашем коде схем/response)

## Формат URL

Внешний путь обычно:

`https://<domain>/<service>/api/v1/<endpoint>`

Примеры:

- `https://<domain>/pixverse/api/v1/text2video`
- `https://<domain>/chatgpt/api/v1/text2photo`
- `https://<domain>/wan/api/v1/status/{id}`

## Медиа

### API-стрим эндпоинт

Для сервисов, где подключен `media_router`, доступен:

- `GET /media/{full_path:path}`

Полный путь:

- `https://<domain>/<service>/api/v1/media/<relative_path>`

Пример:

- `https://<domain>/pixverse/api/v1/media/video/large/<file>.mp4`

### Прямая статика (nginx)

Если настроен `location /static/` c `alias` на каталог `uploads`, можно использовать:

- `https://<domain>/static/video/large/<file>.mp4`
- `https://<domain>/static/photo/<file>.jpg`

## Краткая карта эндпоинтов

Ниже перечислены основные публичные пути (без учета префикса сервиса и `/api/v1`).

### Auth

- `POST /token`
- `POST /refresh`

### Pixverse

- `POST /text2video`
- `POST /image2video`
- `POST /video2video`
- `POST /template2video`
- `POST /extend2video`
- `POST /transition2video`
- `GET /status`
- `GET/POST/PUT/DELETE /styles`
- `GET/POST/PUT/DELETE /templates`
- `GET/POST/PUT/DELETE /applications`
- `GET /get_templates/{app_id}`
- `GET/POST/PUT/DELETE /accounts`
- `GET /statistics`
- `GET /statistics/filters`
- `GET /users/{user_id}/tokens`

### ChatGPT

- `POST /text2photo`
- `POST /photo2photo`
- `POST /template2photo`
- `POST /template2avatar`
- `POST /photo2toybox`
- `POST /edit2reshape`
- `POST /text2post`
- `POST /face2swap`
- `POST /photo2antiques`
- `POST /video2subtitle`
- `POST /video2voice`
- `GET/POST/PUT/DELETE /templates`
- `GET/POST/PUT/DELETE /applications`
- `GET /get_templates/{app_id}`

### Calories

- `POST /text2calories`
- `POST /photo2calories`
- `POST /text2weight`
- `POST /photo2weight`

### Instagram

- `POST /users/session`
- `GET /users/{uuid}/search/{username}`
- `POST /users/{uuid}/tracking/{user_id}`
- `GET /users/{uuid}/tracking`
- `DELETE /users/{uuid}/tracking/{user_id}`
- `GET /tracking/{username}/statistics`
- `GET /tracking/{username}/chart`
- `POST /users/{uuid}/update`
- `GET /users/{uuid}/statistics`
- `GET /users/{uuid}/publications/{id}`
- `GET /users/{username}/publications/{id}`
- `GET /users/{uuid}/subscribers`
- `GET /tracking/{username}/subscribers`
- `GET /users/{uuid}/secret-fans`
- `GET /users/{username}/secret-fans`
- `GET /users/{uuid}/subscribers/chart`
- `GET /users/{uuid}/subscribtions`
- `GET /users/{username}/subscribtions`
- `POST /users/{uuid}/text2post`

### Cosmetic

- `POST /photo2cosmetic`

### Qwen

- `POST /text2photo`
- `POST /photo2photo`
- `GET/POST/PUT/DELETE /accounts`

### Topmedia

- `POST /text2speech`
- `POST /text2song`
- `GET /voices`

### Pika

- `POST /text2video`
- `POST /image2video`
- `POST /template2video`
- `POST /twist2video`
- `POST /addition2video`
- `POST /face2swap`
- `GET /status/{id}`
- `GET /templates`
- `GET /accounts`
- `GET /applications`
- `GET /applications/{app_id}`

### Wan

- `POST /text2image`
- `POST /text2video`
- `POST /image2video`
- `POST /template2video`
- `GET /status/{id}`

### Ximilar

- `POST /card2info`

### Common / Dashboard

- `GET/POST/PUT/DELETE /store_applications`
- `GET/POST/PUT/DELETE /products`
- `POST /webhooks/{webhook_id}`

### Other

- `POST /photo2gamestone`
- `POST /fact2day`
- `POST /photo2location`

## Полезные команды

Перезапуск всех контейнеров:

```bash
docker compose up -d --build --force-recreate
```

Логи сервиса:

```bash
docker compose logs -f chatgpt
```

Проверка медиа-эндпоинта:

```bash
curl -v "https://<domain>/pixverse/api/v1/media/video/large/<file>.mp4" -o test.mp4
```
