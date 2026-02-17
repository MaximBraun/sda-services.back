# !/bin/bash

# ENV_FILE=".env"

# # Загружаем конфигурацию
# if [ ! -f "$ENV_FILE" ]; then
#     echo "ERROR: Configuration file '$ENV_FILE' not found."
#     exit 1
# fi

# export $(grep -v '^#' "$ENV_FILE" | xargs)

# # Проверка переменных
# : "${APP_SERVICE:?APP_SERVICE is not set in .env}"
# : "${APP_HOST:?APP_HOST is not set in .env}"
# : "${APP_PORT:?APP_PORT is not set in .env}"

# echo "INFO: Running FastAPI service '$APP_SERVICE' on ${APP_HOST}:${APP_PORT}"

# # Запуск FastAPI
# uvicorn "services.${APP_SERVICE}.main:main" --reload --factory --host "${APP_HOST}" --port "${APP_PORT}"


load_config() {
    local env_file=".env"

    if [ ! -f "$env_file" ]; then
        echo "ERROR" "Configuration file '$env_file' not found."
        return 1
    fi

    if export $(grep -v '^#' "$env_file" | xargs) > /dev/null 2>&1; then
        echo "INFO" "Application configuration has been loaded successfully."
    fi
}

# Функция для запуска приложения
start_fastapi_app() {
    echo "INFO" "Running Application."
    uvicorn "$@"
}

load_config

start_fastapi_app services.${APP_SERVICE}.main:main --reload --factory --host ${APP_HOST} --port ${APP_PORT}
























