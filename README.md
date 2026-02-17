# Привет всем, я [Степан](https://daniilshat.ru/) ![](https://github.com/blackcater/blackcater/raw/main/images/Hi.gif)

## Описание backend части для платформы — **Pixverse**

Основной стек приложения: `FastAPI`, `Pydantic`, `Selenium`, `Httpx`

### Этапы разработки:

#### 1. Изучение API платформы Pixverse

Я обнаружил, что для интеграции подойдут следующие HTTP эндпоинты:

| Метод | URI                                      | Назначение                          |
|-------|------------------------------------------|-------------------------------------|
| POST  | `/creative_platform/login`               | Авторизация                         |
| POST  | `/creative_platform/video/t2v`           | Генерация видео по тексту           |
| POST  | `/creative_platform/video/i2v`           | Генерация видео по изображению      |

---

Они позволили реализовать бизнес-логику:

* Авторизация на платформе
* Создание видео на основе текста (T2V)
* Создание видео на основе изображения и текста (I2V)

Для запросов я использовал `httpx`, благодаря чему легко реализовал получение `access_token` через `/creative_platform/login`, который далее использовался при генерации видео.

#### 2. Работа с изображениями и статусами генерации

API предоставляет возможность загружать изображения и получать статус генерации видео. Это было реализовано с помощью `httpx` и запросов к:

| Метод | URI                                      | Назначение                          |
|-------|------------------------------------------|-------------------------------------|
| POST  | `/openapi/v2/image/upload`               | Загузка фотографии по API           |
| GET   | `/openapi/v2/video/result/{id}`          | Получение статуса генерации         |

---

#### 3. Генерация через Selenium

Для симуляции пользовательского взаимодействия и получения логов от сервера я использовал `Selenium`. Это позволило отправлять промпты (prompt) и обрабатывать асинхронные ответы.

#### 4. Интеграция в FastAPI

Все модули были объединены и связаны с помощью `FastAPI`, создавая REST API интерфейс.

### ⏱ Время реализации

На реализацию я потратил около суток-двух, так как столкнулся с проблемой развертывания контейнера из-за Selenium:

```Dockerfile
# Установка Google Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && apt-get install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

# Установка ChromeDriver
RUN wget -q --continue -P /tmp "https://storage.googleapis.com/chrome-for-testing-public/${CHROMEDRIVER_VERSION}/linux64/chromedriver-linux64.zip" && \
    unzip /tmp/chromedriver-linux64.zip -d /tmp && \
    mv /tmp/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver && \
    chmod +x /usr/local/bin/chromedriver && \
    rm -rf /tmp/chromedriver-linux64 /tmp/chromedriver-linux64.zip
```

К основным трудностям, с которыми я столкнулся, было получение логов:

```python
def get_logs(
    self,
    api_uri: str,
) -> None:
    """
    Получить логи с ответами от API с указанным URI.
    """

    for request in self._driver.requests:
        if api_uri in request.url and request.response:
            body_bytes = request.response.body
            if not body_bytes:
                continue

            try:
                with GzipFile(fileobj=BytesIO(body_bytes)) as f:
                    text = f.read().decode("utf-8")
            except OSError:
                text = body_bytes.decode("utf-8")

            return loads(text)
```

---

### 📦 Примеры кода API:

#### Авторизация

```python
@pixverse_router.post("/auth")
@auto_docs(...)
async def auth_user(...):
    user = await view.auth_user(body)
    try:
        return AccessToken(access_token=user.response.result.token)
    except Exception:
        raise InvalidCredentials
```

#### Генерация видео по тексту

```python
@pixverse_router.post("/t2v")
@auto_docs(...)
async def text_to_video(...):
    return await view.text_to_video(token, body)
```

#### Генерация видео по изображению

```python
@pixverse_router.post("/i2v")
@auto_docs(...)
async def image_to_video(...):
    return await view.image_to_video(token, body, file)
```

#### Получение статуса генерации

```python
@pixverse_router.post("/status")
@auto_docs(...)
async def generation_status(...):
    return await view.generation_status(body)
```

---

### 📁 Структура URI:

```python
class PixVerseUri(StrEnum):
    AUTH = "/creative_platform/login"
    TEXT = "/creative_platform/video/t2v"
    IMAGE = "/creative_platform/video/i2v"
    UPLOAD = "/openapi/v2/image/upload"
    STATUS = "/openapi/v2/video/result/{id}"
```

---

### 🌐 HTTP клиент с httpx:

```python
class Web3:
    def __init__(self, url: str) -> None:
        self._url = url

    async def get_client(self, headers: dict[str, Any]) -> AsyncGenerator[AsyncClient, Any]:
        async with AsyncClient(headers=headers) as client:
            yield client

    async def __make_request(...):
        ...

    async def send_request(...):
        ...
```

### 🎬 Клиент PixVerse:

```python
class PixVerseCore(Web3):
    def __init__(self):
        super().__init__(PIXVERSE_API_URL)

    async def post(...):
        ...

    async def get(...):
        ...
```

```python
class PixVerseClient:
    def __init__(self, core: PixVerseCore):
        self.core = core

    async def generate_video_from_text(...):
        ...

    async def generate_video_from_image(...):
        ...
```



# sda-services.back
