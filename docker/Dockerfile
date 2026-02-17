FROM python:3.11

ENV PROJECT_DIR="/code" \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CHACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=2.1.1 \
    POETRY_VIRTUALENVS_CREATE=false \
    PATH="${PATH}:/root/.poetry/bin" 

# Установка зависимостей
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    curl \
    unzip \
    apt-transport-https \
    ca-certificates \
    xvfb \
    fonts-liberation \
    libappindicator3-1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libc6 \
    libcairo2 \
    libcups2 \
    libdbus-1-3 \
    libgdk-pixbuf-xlib-2.0-0 \
    libnspr4 \
    libnss3 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libgtk-3-0 \
    libxss1 \
    lsb-release \
    xdg-utils \
    libu2f-udev \
    libvulkan1 \
    ffmpeg \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*


# Установка Poetry
RUN pip install --upgrade pip==24.0 && \
    pip install poetry==$POETRY_VERSION && \
    poetry --version

# Установка рабочей директории
WORKDIR $PROJECT_DIR

# Копирование зависимостей
COPY ./pyproject.toml ./poetry.lock ${PROJECT_DIR}/

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root

# Копирование проекта
COPY . ${PROJECT_DIR}/
