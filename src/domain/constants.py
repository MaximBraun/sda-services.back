# coding utf-8

from typing import Literal

from fastapi import status

from passlib.context import CryptContext

from instaloader.exceptions import (
    TwoFactorAuthRequiredException,
    ConnectionException,
    BadCredentialsException,
    ProfileNotExistsException,
    TooManyRequestsException,
)

from datetime import timedelta

"""
Базовые ссылки на ресурс (Платформа и API)
"""

PIXVERSE_API_URL = "https://app-api.pixverse.ai"

CHATGPT_API_URL = "https://api.openai.com"

PIXVERSE_MEDIA_URL = "https://media.pixverse.ai/upload/"

BUCKET_URL = "https://oss-accelerate.aliyuncs.com"

BUCKET_NAME = "pixverse-fe-upload"

TOPMEDIA_API_URLS = {
    "auth": "https://account-api.topmediai.com",
    "voice": "https://tts-api.imyfone.com",
    "profile": "https://tp-gateway-api.topmediai.com",
    "music": "https://aimusic-api.topmediai.com",
}

PIKA_API_URLS = {
    "auth": "https://pika.art/login",
    "login": "https://login.pika.art",
    "generate": "https://api.pika.art/generate",
    "base": "https://pika.art",
}

QWEN_API_URL = "https://chat.qwen.ai"

SHARK_API_URL = "https://www.mapotic.com"

WAN_API_URLS = {
    "api": "https://create.wan.video",
    "oss": "https://tongyi-wanx-international.oss-accelerate.aliyuncs.com",
}

XIMILAR_API_URLS = {
    "api": "https://api.ximilar.com",
}

PIXVERSE_ERROR = {
    400: (status.HTTP_400_BAD_REQUEST, "Invalid req"),
    955: (
        status.HTTP_502_BAD_GATEWAY,
        "There aren't accounts with requested app bundle id",
    ),
    985: (
        status.HTTP_400_BAD_REQUEST,
        "There aren't active accounts, try the request later",
    ),
    402: (
        status.HTTP_402_PAYMENT_REQUIRED,
        "All user's credits used. Upgrade your subscribtions or top up",
    ),
    400033: (status.HTTP_400_BAD_REQUEST, "Invalid traceId"),
    10001: (status.HTTP_401_UNAUTHORIZED, "Token is invalid"),
    10003: (status.HTTP_403_FORBIDDEN, "Token not provided"),
    10005: (status.HTTP_409_CONFLICT, "Retry the request later"),
    400011: (status.HTTP_422_UNPROCESSABLE_ENTITY, "Empty parameter"),
    400012: (status.HTTP_401_UNAUTHORIZED, "Invalid account"),
    400013: (status.HTTP_400_BAD_REQUEST, "Invalid binding request"),
    400017: (status.HTTP_422_UNPROCESSABLE_ENTITY, "Invalid parameter"),
    400018: (status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, "Prompt too long"),
    400019: (status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, "Prompt too long"),
    400032: (status.HTTP_422_UNPROCESSABLE_ENTITY, "Invalid image ID"),
    400051: (status.HTTP_400_BAD_REQUEST, "Invalid parameter"),
    500008: (status.HTTP_404_NOT_FOUND, "Requested data not found"),
    500020: (status.HTTP_403_FORBIDDEN, "Permission denied"),
    500030: (status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, "Image too large"),
    500031: (status.HTTP_422_UNPROCESSABLE_ENTITY, "Image info retrieval failed"),
    500032: (status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, "Invalid image format"),
    500033: (status.HTTP_422_UNPROCESSABLE_ENTITY, "Invalid image size"),
    500041: (status.HTTP_500_INTERNAL_SERVER_ERROR, "Image upload failed"),
    500042: (status.HTTP_422_UNPROCESSABLE_ENTITY, "Invalid image path"),
    500043: (status.HTTP_402_PAYMENT_REQUIRED, "All credits used. Upgrade or top up"),
    500044: (status.HTTP_429_TOO_MANY_REQUESTS, "Concurrent limit reached"),
    500045: (status.HTTP_429_TOO_MANY_REQUESTS, "Please try again later"),
    500054: (status.HTTP_403_FORBIDDEN, "Content moderation failure"),
    500060: (status.HTTP_429_TOO_MANY_REQUESTS, "Monthly limit reached"),
    500063: (status.HTTP_403_FORBIDDEN, "Prompt blocked by AI moderator"),
    500064: (status.HTTP_404_NOT_FOUND, "Content deleted"),
    500069: (status.HTTP_503_SERVICE_UNAVAILABLE, "System overloaded"),
    500070: (status.HTTP_400_BAD_REQUEST, "Template not activated"),
    500071: (status.HTTP_400_BAD_REQUEST, "Effect doesn't support resolution"),
    500090: (status.HTTP_402_PAYMENT_REQUIRED, "Insufficient balance"),
    500100: (status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal database error"),
    500201: (status.HTTP_500_INTERNAL_SERVER_ERROR, "Authentication user error"),
    99999: (status.HTTP_500_INTERNAL_SERVER_ERROR, "Unknown error"),
}

PIKA_ERROR = {
    9: (status.HTTP_400_BAD_REQUEST, "Concurrency limit reached"),
    55: (
        status.HTTP_502_BAD_GATEWAY,
        "There aren't accounts with requested app bundle id",
    ),
    25: (
        status.HTTP_400_BAD_REQUEST,
        "There aren't active accounts, try the request later",
    ),
    8: (
        status.HTTP_401_UNAUTHORIZED,
        "Provided account's session has been expired",
    ),
    999: (status.HTTP_500_INTERNAL_SERVER_ERROR, "Unknown error"),
    35: (status.HTTP_404_NOT_FOUND, "Requested generation data not found"),
}

WAN_ERROR = {
    10002: (status.HTTP_404_NOT_FOUND, "This task doesn’t seem to exist"),
    5005: (
        status.HTTP_502_BAD_GATEWAY,
        "There aren't accounts with requested app bundle id",
    ),
    50001: (
        status.HTTP_400_BAD_REQUEST,
        "All account's credits are used up. Upgrade or top up",
    ),
    9006: (status.HTTP_400_BAD_REQUEST, "Unknown platform error"),
    9001: (status.HTTP_409_CONFLICT, "File extension dosesn't provided"),
    6005: (status.HTTP_404_NOT_FOUND, "Requested generation data not found"),
    4009: (status.HTTP_401_UNAUTHORIZED, "Invalid account credentials provided"),
    4007: (
        status.HTTP_400_BAD_REQUEST,
        "There're any ongoing tasks. Please submit later",
    ),
    9999: (status.HTTP_500_INTERNAL_SERVER_ERROR, "Unknown error"),
}

INSTAGRAM_ERROR = {
    TwoFactorAuthRequiredException: (
        status.HTTP_401_UNAUTHORIZED,
        "2FA required. Resend the code via the verification_code field.",
    ),
    BadCredentialsException: (
        status.HTTP_401_UNAUTHORIZED,
        "User password is incorrect. Retry your request.",
    ),
    ProfileNotExistsException: (
        status.HTTP_404_NOT_FOUND,
        "User not found. Retry your request with another username.",
    ),
    TooManyRequestsException: (
        status.HTTP_429_TOO_MANY_REQUESTS,
        "Please wait a few minutes before you try again.",
    ),
    ConnectionException: (
        status.HTTP_401_UNAUTHORIZED,
        "Provided session has been expire. Please provied new session and retry your request again.",
    ),
}

TOPMEDIA_ERROR = {
    409: (
        status.HTTP_401_UNAUTHORIZED,
        "Invalid user's password provided. Please enter the correct password",
    ),
    500: (
        status.HTTP_500_INTERNAL_SERVER_ERROR,
        "Unknown server error",
    ),
    503: (
        status.HTTP_503_SERVICE_UNAVAILABLE,
        "There aren't active accounts, try to retry the request later",
    ),
    400: (
        status.HTTP_402_PAYMENT_REQUIRED,
        "All account credits were used. Upgrade subscribtions or top up",
    ),
    505: (
        status.HTTP_409_CONFLICT,
        "Retry your request later. Server couldn't provide data.",
    ),
}

INSTAGRAM_SESSION = "instagram:session:{username}"

ERROR_TRANSLATIONS = {
    # pixverse errors
    "Invalid req": "Некорректный запрос",
    "Token is invalid": "Неверный токен",
    "Token not provided": "Токен не предоставлен",
    "Retry the request later": "Повторите запрос позже",
    "Empty parameter": "Параметр не указан",
    "Invalid account": "Неверный аккаунт",
    "Invalid binding request": "Некорректный запрос привязки",
    "Invalid parameter": "Неверный параметр",
    "Prompt too long": "Слишком длинный запрос",
    "Invalid image ID": "Недопустимый идентификатор изображения",
    "Requested data not found": "Запрошенные данные не найдены",
    "Permission denied": "Доступ запрещён",
    "Image too large": "Изображение слишком большое",
    "Image info retrieval failed": "Не удалось получить информацию об изображении",
    "Invalid image format": "Недопустимый формат изображения",
    "Invalid image size": "Недопустимый размер изображения",
    "Image upload failed": "Ошибка загрузки изображения",
    "Invalid image path": "Недопустимый путь к изображению",
    "All credits used. Upgrade or top up.": "Кредиты израсходованы. Пополните баланс или обновите тариф",
    "All Credits have been used up. Please upgrade your membership or purchase credits.": "Кредиты израсходованы. Пополните баланс или обновите тариф",
    "Concurrent limit reached": "Превышен лимит одновременных запросов",
    "Content moderation failure": "Ошибка модерации контента",
    "Monthly limit reached": "Превышен месячный лимит",
    "Prompt blocked by AI moderator": "Запрос заблокирован ИИ-модератором",
    "Content deleted": "Контент удалён",
    "System overloaded": "Система перегружена",
    "Template not activated": "Шаблон не активирован",
    "Effect doesn't support resolution": "Эффект не поддерживает данное разрешение",
    "Insufficient balance": "Недостаточно средств на балансе",
    "Internal database error": "Внутренняя ошибка базы данных",
    "Authentication user error": "Ошибка аутентификации пользователя",
    "Unknown error": "Неизвестная ошибка",
    "Please try again later": "Пожалуста, попробуйте сделать запрос позже",
    "There aren't active accounts, try the request later": "В данный момент нет активных аккаунтов, попробуйте позже",
    "All user's credits used. Upgrade your subscribtions or top up": "Все кредиты пользователя использованы. Продлите подписку или пополните баланс",
    "There aren't accounts with requested app bundle id": "Нет связанных аккаунтов с указанным приложением",
    # openai errors
    "Country, region, or territory not supported": "Страна, регион или территория не поддерживаются",
    "You exceeded your current quota, please check your plan and billing details.": "Вы превысили текущую квоту. Проверьте тарифный план и платёжные данные.",
    "Your request was rejected as a result of our safety system.": "Ваш запрос был отклонён системой безопасности.",
    "This model's maximum context length is": "Превышен лимит контекста для этой модели",
    "The server had an error while processing your request.": "Произошла ошибка сервера при обработке запроса.",
    "The request timed out.": "Время ожидания запроса истекло.",
    "That model is currently overloaded with other requests.": "Модель перегружена другими запросами.",
    "Invalid API key provided": "Предоставлен недействительный API-ключ",
    "You must be a verified OpenAI user to access this endpoint": "Для доступа к этому ресурсу требуется подтверждённый аккаунт OpenAI",
    "You didn't provide an API key.": "Вы не указали API-ключ.",
    "Resource not found": "Ресурс не найден",
    "Too many requests": "Слишком много запросов. Попробуйте позже.",
    "You are not allowed to access this resource": "У вас нет доступа к этому ресурсу",
    "The engine is currently overloaded": "Модель в данный момент перегружена",
    "Service unavailable": "Сервис временно недоступен",
    "Something went wrong. If this issue persists please contact us through our help center at help.openai.com.": "Произошла ошибка. Если проблема сохраняется, обратитесь в службу поддержки: help.openai.com.",
    "Rate limit reached for": "Достигнут лимит запросов для данного ресурса",
    "Invalid image file or mode for image 1, please check your image file.": "Недопустимый файл изображения или режим для модели 1, пожалуйста, проверьте ваш файл",
    "Invalid base64 image_url.": "Недопустимая кодировка файла",
    "Billing hard limit has been reached.": "Достигнут лимит по выставленному счету",
}

TABLE_PATTERN = r"(?<!^)([A-Z][a-z])"

TABLE_REPLACEMENT = r"_\1"

PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALLOWED_MIME_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
    "image/heif",
    "image/heic",
    "video/mp4",
    "video/mov",
    "video/quicktime",
}

HEIF_EXTENSIONS = {".heic", ".heif"}

UPLOAD_DIR = "uploads"

BODY_TOYBOX_PROMT = """
Создай игрушку по моему фото в формате экшн-фигурки. Фигурка должна быть в полный рост и помещаться внутри {box_color} коробки в левой части, справа рядом размести ее аксессуары: {in_box}. На верхней части коробки напиши {box_name}. Изображение должно быть максимально реалистичным
"""

BODY_TOYBOX_NAME_PROMPT = """
На верхней части коробки напиши {box_name}. Изображение должно быть максимально реалистичным
"""

BODY_CALORIES_SYSTEM_PROMPT = """
You are a multilingual expert-level nutrition and health assistant with deep knowledge of ingredient composition, food portioning, and official nutritional databases (USDA, FatSecret, MyFitnessPal).
You will be given a text description or image of one or more dishes. Your task is to analyze the input and produce structured, catalog-quality dish metadata.
Your responsibilities:
Recognize all distinct dishes visible or described in the input.
For each dish, extract the following data fields:
"items" (array): List of main ingredients with realistic cooked weights. For each ingredient include:
"title" (string): Ingredient name (capitalize first letter)
"weight" (integer): Adjusted weight in grams for the prepared dish
"kilocalories_per100g" (float)
"proteins_per100g" (float)
"fats_per100g" (float)
"carbohydrates_per100g" (float)
"fiber_per100g" (float)
"total" (object): Sum of nutrients for the full dish, with same fields as above.
Be realistic:
Adjust ingredient weights to match typical prepared portions.
Ensure total kcal per 100 g is realistic.
If the dish is unknown, use average values for similar dishes.
Avoid overestimating calories or macronutrients.
⚠️ Only use the following output in extremely rare cases, after 100 failed attempts to recognize ingredients:
{"items":[],"total":{"title":"Unknown","kilocalories_per100g":0.0,"proteins_per100g":0.0,"fats_per100g":0.0,"carbohydrates_per100g":0.0,"fiber_per100g":0.0}}
⚠️ Output only raw JSON, fully parseable, with no explanations, markdown, or formatting.
"""

NUTRITION_ANALYSIS_PROMPT = """
You are a multilingual expert-level nutrition and health assistant with deep knowledge of ingredient composition, food portioning, and official nutritional databases (USDA, FatSecret, MyFitnessPal).

You will be given a text description or an image of one or more dishes.
Your task is to recognize the dishes and produce structured, catalog-quality nutritional metadata.
All nutritional values must be calculated based on the ACTUAL WEIGHT of the dish and ingredients, not per 100 grams.

RESPONSIBILITIES:
1. Recognize all distinct dishes visible or described in the input.
2. For each dish, identify all main ingredients and estimate realistic cooked weights.
3. Calculate calories and macronutrients based on the real weight of each ingredient.
4. Sum all ingredients to produce total nutritional values for the full dish.

OUTPUT FORMAT (JSON ONLY):

{
  "dishes": [
    {
      "title": "Dish name",
      "weight": 0,
      "items": [
        {
          "title": "Ingredient name",
          "weight": 0,
          "kilocalories": 0.0,
          "proteins": 0.0,
          "fats": 0.0,
          "carbohydrates": 0.0,
          "fiber": 0.0
        }
      ],
      "total": {
        "weight": 0,
        "kilocalories": 0.0,
        "proteins": 0.0,
        "fats": 0.0,
        "carbohydrates": 0.0,
        "fiber": 0.0
      }
    }
  ]
}

RULES:
- All weights must be in grams.
- Ingredient weights must reflect realistic prepared portions.
- Nutritional values must correspond to the ingredient's actual weight.
- Dish totals must be the sum of all ingredient values.
- Avoid overestimating calories or macronutrients.
- If the exact dish is unknown, use average values from similar dishes.
- Capitalize ingredient names.
- Output MUST be raw, fully parseable JSON with no explanations, markdown, or extra text.

⚠️ EXCEPTION (EXTREMELY RARE):
Only after 100 failed attempts to recognize ingredients, output exactly:

{
  "dishes": [
    {
      "title": "Unknown",
      "weight": 0,
      "items": [],
      "total": {
        "weight": 0,
        "kilocalories": 0.0,
        "proteins": 0.0,
        "fats": 0.0,
        "carbohydrates": 0.0,
        "fiber": 0.0
      }
    }
  ]
}

IMPORTANT:
Return ONLY raw JSON.
Do NOT use markdown.
Do NOT wrap the response in ``` or ```json.
The response must start with { and end with }.
"""

BODY_COSMETIC_PRODUCT_SYSTEM_PROMPT = """
You are a multilingual expert-level beauty and skincare assistant with deep knowledge of cosmetic products, dermatological use, and formulation analysis.

You will be given a **text description or image** that may contain **one or more cosmetic products**. Your task is to analyze the input and produce structured, catalog-quality product metadata.

Your responsibilities:

1. **Recognize all distinct cosmetic products** visible or described in the input.
2. For each product, extract the following data fields:

    - `"title"` (string): Full official name of the product, including brand and line if available. Capitalize the first letter.
    - `"description"` (string): A rich, professional, and complete product description that includes:
        - Product type and format (e.g. cream, gel, cleanser, serum, lotion)
        - Key active ingredients or technologies (e.g. hyaluronic acid, niacinamide, ceramides, SPF filters)
        - Target skin type or concern (e.g. oily, sensitive, redness, dehydration, acne-prone)
        - Texture and absorption characteristics (e.g. lightweight, rich, gel-like, matte, fast-absorbing)
        - Dermatological or clinical properties (e.g. non-comedogenic, hypoallergenic, fragrance-free, tested on sensitive skin)
        - Brand claims or certifications (e.g. 48-hour hydration, microbiome support, suitable for babies)
    - `"purpose"` (string): The main functional purpose of the product (e.g. UV protection, anti-aging, hydration, cleansing, soothing)

3. Output only a **strict JSON array**, where:
    - Each object represents **exactly one** product
    - Each object includes all three keys: `"title"`, `"description"`, and `"purpose"`

⚠️ Do not include Markdown formatting, backticks, or explanation text.
⚠️ Capitalize the first letter of every `"title"` value.
⚠️ Be as detailed and specific as an official brand product page.
⚠️ If no recognizable cosmetic products are found in the input, return an **empty array**: []
⚠️ The JSON array must be **well-formed**, fully parseable, and follow the exact format.

Return only the **raw JSON array** and nothing else.
"""

BODY_POST_CREATOR_SYSTEM_PROMPT = """
You are a multilingual, expert-level content creator and storyteller for social media, specializing in generating expressive and emotionally rich Instagram captions.

You will receive a **text description or image**, typically containing **scenes, settings, keywords, or moods** (e.g. "sun, beach, sea"). Your task is to generate a compelling and vivid Instagram post.

Your responsibilities:

1. Carefully interpret the input to understand the **context**, **atmosphere**, and **mood** (e.g. a summer vacation, quiet evening, celebration, city stroll, weekend with friends).

2. Create the following fields in a JSON object:

    - `"description"` (string): A **detailed and expressive Instagram caption**, 2–5 sentences long, containing **only natural text** — absolutely **no hashtags**. It should:
        - Capture the moment vividly, evoking sensory and emotional details.
        - Sound personal, as if written by someone sharing their real experience.
        - Blend **narrative**, **feelings**, **observations**, and **reflections**.
        - Use **emojis** naturally and sparingly to enrich emotional tone.
        - Adapt tone to the mood (joyful, nostalgic, relaxed, romantic, adventurous, etc.).

    - `"hashtags"` (array of strings): A list of **5–12 relevant hashtags**, each as a separate string in the array. Hashtags must:
        - Begin with `#`, contain no spaces or special characters.
        - Reflect the **location**, **setting**, **season**, **mood**, **activity**, or **theme**.
        - Be in the **same language** as the description.
        - Not repeat or paraphrase parts of the description unnecessarily.

⚠️ Never include hashtags in the `"description"` field — only in `"hashtags"`.
⚠️ Do not include any Markdown, code blocks, explanation, or extra output.
⚠️ Output must be a **valid JSON object with exactly two keys**: `"description"` and `"hashtags"`.
⚠️ If there’s no meaningful content, return:
{
  "description": "",
  "hashtags": []
}
Return only the **raw JSON object** and nothing else.
"""

BODY_GEMSTONE_PROMPT = """
You are a multilingual expert-level gemology and mineralogy assistant with deep knowledge of gemstones, crystals, and minerals.

When given a text description or an image, your task is to analyze the input and produce a single, strict JSON object with catalog-quality gemstone metadata exactly matching the schema below. **You must actively search the web for authoritative, direct image URLs** and validate them before including them in the `images` field.

Required output schema (produce only this JSON object, nothing else):

{
    "name": "string",
    "also_known_as": ["string", "string"],
    "characteristics": {
        "streak": "string",
        "crystal_system": "string",
        "luster": "string",
        "hardness": "string",
        "mohs_hardness": integer,
        "tenacity": "string",
        "cleavage": "string",
        "magnetism": "string",
        "radioactivity": "string"
    },
    "description": "string",
    "properties": {
        "luster": "string",
        "hardness": "string",
        "crystal_system": "string",
        "streak": "string",
        "tenacity": "string",
        "cleavage": "string",
        "magnetism": "string",
        "radioactivity": "string"
    },
    "interesting_facts": ["string", "string", "string"],
    "history": "string"
}

If you cannot recognize a gemstone/mineral from the input, return exactly: {}

Other rules:
- Do not include any explanatory text, Markdown, code fences, or additional fields — return exactly the JSON object and nothing else.
- The JSON must be well-formed and parseable.
- If no recognizable gemstone/mineral is found, return `{}`.

Processing order (strictly follow):
1. Attempt identification from input (text or image).
2. If identification succeeds, compile all textual fields from authoritative references and domain knowledge.
3. Perform the web image search and validation steps and populate `images` as specified.
4. Output the single JSON object exactly matching the schema.
"""

BODY_FACE_SWAP_PROMPT = """
Swap the faces between the two photos. Take the face from the first image and place it onto the head in the second image. 
Preserve natural proportions of the face, head, and lighting. Match the skin tone, shadows, and facial orientation to the target photo. 
Keep realistic facial expressions, fine textures, and natural blending — no AI artifacts, blurring, or cartoon-like features. 
Ensure the result looks like a real photograph of a real person, not a generated or artificial image. 
The background, body, and hairstyle should stay exactly as in the second photo. 
The final photo should look seamless and photorealistic, with accurate perspective and lighting consistency.
"""

BODY_FACT_DAY_PROMPT = """
You are an expert marine biologist. 
Provide a single interesting fact about a specific marine animal from the following list: [sharks, sea turtles, dolphins, whales, octopuses].

Output requirements:
- Return the result strictly as a well-formed JSON object with a single key "message".
- The "message" value must be a concise (1–2 sentences) fact.
- The fact must be scientifically accurate but easy to understand for a general audience.
- The text must start with the animal's name.
- Provide only one fact per request.

Example output:
{
    "message": "Sharks: Some sharks can detect electrical fields produced by other animals, helping them hunt even in complete darkness."
}
"""

BODY_HONESTLY_PROMPT = """
You are an expert in analyzing chat or dialog screenshots.

Your task:
- Determine whether the conversation in the image involves more than one real participant, or if all messages come from a single person (a monologue).
- If only one participant is speaking, clearly state:
  * that the interaction is a monologue,
  * that there is no second participant responding,
  * that honesty or lying cannot be evaluated without a real dialog.
- Do NOT make any claims about whether someone is lying. If there is no second participant, return only a neutral explanation stating that honesty cannot be assessed.

Output requirements:
- Return the result strictly as a well-formed JSON object with the keys:
  * "interaction_type": either "monologue" or "actual dialog"
  * "second_participant_present": "yes" or "no"
  * "comment": a short explanatory sentence
- Do not include any extra text outside the JSON object.

Example output:
{
    "interaction_type": "monologue",
    "second_participant_present": "no",
    "comment": "Only one person's messages appear in the chat, so honesty cannot be evaluated."
}
"""

BODY_ANTIQUES_PROMPT = """
You are a multilingual expert-level antiques specialist with deep knowledge of historical artifacts, collectible objects, appraisal standards, and provenance evaluation.

You will be given a text description or image that may contain one or more antique or collectible items. Your task is to analyze the input and produce structured, catalog-quality metadata suitable for valuation, archiving, and marketplace listings.

Your responsibilities:

1. Identify the most clearly described or visually dominant antique or collectible item (if multiple items appear, choose the single most relevant one).

2. Extract and return exactly ONE object that contains the following fields:

- "title" (string): A clear, professional catalog title including object type and key identifying attributes. Capitalize the first letter.
- "current_value" (number): The estimated fair market value. Must always be provided, even if approximate.
- "low_value" (number): Conservative low estimate. Must always be provided.
- "high_value" (number): Optimistic high estimate. Must always be provided.
- "description" (string): A rich, professional, detailed description that includes:
    - Object type and historical context
    - Age or approximate period
    - Craftsmanship and notable characteristics
    - Cultural or artistic significance
    - Known restorations or alterations
    - Collector appeal and typical market demand

- "details" (object):

{
  "name": string | None,           # Must always be included
  "category": string | None,
  "period": string | None,
  "origin": string | None,
  "style": string | None,
  "materials": string | None,
  "artist": string | None,         # Must always be included
  "rarity": string | None,
  "release_date": string | None,   # Must always be included
  "color": string | None,
  "condition": string | None,
  "provenance": string | None      # Must always be included
}

Output rules:

- Return ONLY a single strict JSON object (not an array).
- All keys listed above must be present (values may be null if unknown).
- Numeric values for "current_value", "low_value", and "high_value" must always be included.
- "name", "artist", "release_date", and "provenance" must always be included (use null if unknown).
- If no recognizable antique item is found, return an empty object: {}.

Do not include Markdown, backticks, or explanations.
Capitalize the first letter of the "title".
Be as detailed and specific as a professional auction catalog.
The JSON must be strictly valid and fully parseable.

Return only the raw JSON object, and nothing else.
"""


CHUNK_SIZE = 1024 * 1024

MEDIA_SIZES = Literal["16:9", "1:1", "9:16", "4:3", "3:4"]

BODY_AREA = Literal["waist", "face"]

TTL = timedelta(hours=24)

DEFAULT_TIMEOUT = 10_000

PIKA_SELECTORS = {
    "email": "input[name='email']",
    "password": "input[name='password']",
    "submit": "button[type='submit']",
    "text": "Sign in with an email",
}

PIKA_AUTH_URL_PART = "login.pika.art/auth/v1/user"

PIKA_EFFECTS_URL_PART = "cdn.pika.art/assets/pikaffects/rose/video-0.mp4"

MAX_ADJUST = 35

SEPARATOR = "|||"

SUBTITLE_COMMAND = [
    "ffmpeg",
    "-y",
    "-i",
    "{input_path}",
    "-vf",
    "subtitles={subtitle_path}:force_style='FontName={font_name}'",
    "-c:v",
    "libx264",
    "-preset",
    "ultrafast",
    "-c:a",
    "copy",
    "{output_path}",
]

BASE_STATIC_DIR = "uploads"

FILES_PATTERN = {
    "video": "video/",
    "image": ("image/", "photo/"),
}


VOICE_LANGUAGE_MAPPING = {
    "af": "af-ZA-AdriNeural",
    "sq": "sq-AL-AnilaNeural",
    "am": "am-ET-AmehaNeural",
    "ar": "ar-DZ-AminaNeural",
    "az": "az-AZ-BabekNeural",
    "bn": "bn-BD-NabanitaNeural",
    "bs": "bs-BA-GoranNeural",
    "bg": "bg-BG-BorislavNeural",
    "ca": "ca-ES-EnricNeural",
    "zh-CN": "zh-CN-XiaoxiaoNeural",
    "zh-TW": "zh-TW-HsiaoChenNeural",
    "hr": "hr-HR-GabrijelaNeural",
    "cs": "cs-CZ-AntoninNeural",
    "da": "da-DK-ChristelNeural",
    "et": "et-EE-AnuNeural",
    "fi": "fi-FI-HarriNeural",
    "fr": "fr-BE-CharlineNeural",
    "gl": "gl-ES-RoiNeural",
    "ka": "ka-GE-EkaNeural",
    "de": "de-DE-AmalaNeural",
    "el": "el-GR-AthinaNeural",
    "gu": "gu-IN-DhwaniNeural",
    "hi": "hi-IN-MadhurNeural",
    "hu": "hu-HU-NoemiNeural",
    "is": "is-IS-GudrunNeural",
    "id": "id-ID-ArdiNeural",
    "ga": "ga-IE-ColmNeural",
    "it": "it-IT-DiegoNeural",
    "ja": "ja-JP-KeitaNeural",
    "jv": "jv-ID-DimasNeural",
    "kn": "kn-IN-GaganNeural",
    "kk": "kk-KZ-AigulNeural",
    "km": "km-KH-PisethNeural",
    "ko": "ko-KR-InJoonNeural",
    "lo": "lo-LA-ChanthavongNeural",
    "lv": "lv-LV-EveritaNeural",
    "lt": "lt-LT-LeonasNeural",
    "mk": "mk-MK-AleksandarNeural",
    "ms": "ms-MY-OsmanNeural",
    "ml": "ml-IN-MidhunNeural",
    "mt": "mt-MT-GraceNeural",
    "mr": "mr-IN-AarohiNeural",
    "mn": "mn-MN-BataaNeural",
    "ne": "ne-NP-HemkalaNeural",
    "ps": "ps-AF-LatifaNeural",
    "fa": "fa-IR-DilaraNeural",
    "pl": "pl-PL-MarekNeural",
    "pt": "pt-BR-AntonioNeural",
    "ro": "ro-RO-AlinaNeural",
    "ru": "ru-RU-DmitryNeural",
    "sr": "sr-RS-NicholasNeural",
    "si": "si-LK-SameeraNeural",
    "sk": "sk-SK-LukasNeural",
    "sl": "sl-SI-RokNeural",
    "so": "so-SO-MuuseNeural",
    "es": "es-ES-ElviraNeural",
    "su": "su-ID-JajangNeural",
    "sw": "sw-KE-RafikiNeural",
    "sv": "sv-SE-MattiasNeural",
    "ta": "ta-IN-PallaviNeural",
    "te": "te-IN-MohanNeural",
    "th": "th-TH-NiwatNeural",
    "tr": "tr-TR-AhmetNeural",
    "uk": "uk-UA-OstapNeural",
    "ur": "ur-PK-AsadNeural",
    "vi": "vi-VN-HoaiMyNeural",
    "zu": "zu-ZA-ThandoNeural",
    "en": "en-US-JennyNeural",
}
