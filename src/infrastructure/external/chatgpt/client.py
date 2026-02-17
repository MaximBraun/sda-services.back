# coding utf-8

import os

from fastapi import UploadFile

from asyncio import sleep

from base64 import b64encode

from io import BytesIO

from PIL import Image

from .core import ChatGPTCore

from ....domain.conf import app_conf

from ....domain.errors import (
    PixverseError,
    PhotoGeneratorError,
)

from ....domain.entities.core import IConfEnv

from ...orm.database.repositories import (
    PhotoGeneratorTemplateRepository,
    UserGenerationRepository,
    UserDataRepository,
)

from ...orm.database.models import PhotoGeneratorTemplates

from ....domain.repositories import IDatabase

from ....domain.tools import (
    upload_chatgpt_file,
    upload_chatgpt_files,
    b64_json_to_image,
    convert_heic_to_jpg,
)

from ....domain.entities.chatgpt import (
    IBody,
    T2PBody,
    PhotoBody,
    TB2PBody,
    R2PBody,
    I2CBody,
    IFaceSwapData,
    R2PBodyPrompt,
    AntiquesBody,
)

from ....domain.typing.enums import ChatGPTEndpoint

from ....interface.schemas.api import Template

from ....interface.schemas.external import (
    ChatGPTResponse,
    ChatGPTResp,
    ChatGPTErrorResponse,
    ChatGPTError,
    GenerationData,
    UsrData,
    ChatGPTAntiquesResponse,
    Antiques,
)

from ....domain.constants import BODY_TOYBOX_PROMT, HEIF_EXTENSIONS


conf: IConfEnv = app_conf()


templates_database = PhotoGeneratorTemplateRepository(
    engine=IDatabase(conf),
)

user_generations_database = UserGenerationRepository(
    engine=IDatabase(conf),
)

user_data_database = UserDataRepository(
    engine=IDatabase(conf),
)


class ChatGPTClient:
    """Клиентский интерфейс для работы с ChatGPT API.

    Предоставляет удобные методы для основных операций с видео контентом:
    - Генерация видео из текста
    - Создание видео из изображений
    - Проверка статуса задач

    Args:
        core (ChatGPTCore): Базовый клиент для выполнения запросов
    """

    def __init__(
        self,
        core: ChatGPTCore,
    ) -> None:
        self._core = core

    async def __handle_success(
        self,
        user_data: IBody | TB2PBody | T2PBody,
        data: ChatGPTResponse,
    ) -> ChatGPTResp:
        video_data = ChatGPTResp(
            url=b64_json_to_image(data.data[0].b64_json),
        )
        await user_generations_database.add_record(
            GenerationData(
                user_id=user_data.user_id,
                app_id=user_data.app_id,
                app_name=os.getenv("APP_SERVICE", "chatgpt").lower(),
                generation_url=video_data.url,
            )
        )
        await user_data_database.create_or_update_user_data(
            UsrData(
                user_id=user_data.user_id,
                app_id=user_data.app_id,
            )
        )
        return video_data

    async def file_to_base64(self, file: UploadFile) -> str:
        data = await file.read()
        b64 = b64encode(data).decode()
        mime = file.content_type
        return f"data:{mime};base64,{b64}"

    async def build_swap_payload(
        self, image1: UploadFile, image2: UploadFile, prompt: str
    ):
        img1_b64 = await self.file_to_base64(image1)
        img2_b64 = await self.file_to_base64(image2)

        return {
            "model": "gpt-4.1",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "input_image", "image_url": img1_b64},
                        {"type": "input_image", "image_url": img2_b64},
                    ],
                }
            ],
        }

    async def __handle_failure(
        self,
        last_error: ChatGPTError | str,
        status_code: int | None = None,
        extra: dict[str] = {},
    ) -> PhotoGeneratorError:
        error = PhotoGeneratorError(
            status_code=status_code if status_code is not None else 400,
            detail=last_error.message
            if isinstance(last_error, ChatGPTError)
            else last_error,
            extra=extra,
        )

        raise error

    async def text_to_photo(
        self,
        body: IBody,
        prompt: str,
    ) -> ChatGPTResp:
        max_attempts = 10

        last_error = None

        for attempt in range(max_attempts):
            token = conf.chatgpt_token
            try:
                data: ChatGPTResponse | ChatGPTErrorResponse = await self._core.post(
                    token=token,
                    endpoint=ChatGPTEndpoint.TEXT,
                    body=PhotoBody(
                        prompt=body.prompt if prompt is None else prompt,
                    ),
                )

                if isinstance(data, ChatGPTErrorResponse):
                    last_error = data.error
                else:
                    return await self.__handle_success(
                        body,
                        data,
                    )

            except Exception as err:
                last_error = str(err)

            if attempt < max_attempts - 1:
                await sleep(1)

        return await self.__handle_failure(
            last_error,
            extra={"Токен авторизации": token},
        )

    async def photo_to_photo(
        self,
        body: IBody,
        image: UploadFile,
        prompt: str,
    ) -> ChatGPTResp:
        max_attempts = 10

        last_error = None

        files = await upload_chatgpt_file(
            body,
            image,
            prompt,
        )

        for attempt in range(max_attempts):
            token = conf.chatgpt_token
            try:
                data: ChatGPTResponse | ChatGPTErrorResponse = await self._core.post(
                    token=token,
                    endpoint=ChatGPTEndpoint.PHOTO,
                    files=files,
                )

                if isinstance(data, ChatGPTErrorResponse):
                    last_error = data.error
                else:
                    return await self.__handle_success(
                        body,
                        data,
                    )

            except Exception as err:
                last_error = str(err)

            if attempt < max_attempts - 1:
                await sleep(1)

        return await self.__handle_failure(
            last_error,
            extra={"Токен авторизации": token},
        )

    async def template_to_photo(
        self,
        body: T2PBody,
        image: UploadFile,
    ) -> ChatGPTResp:
        max_attempts = 10

        last_error = None

        template: Template | None = await templates_database.fetch_template(
            "id",
            body.id,
        )
        if template is None:
            raise PixverseError(
                status_code=500070,
            )

        files = await upload_chatgpt_file(
            template,
            image,
        )

        for attempt in range(max_attempts):
            token = conf.chatgpt_token
            try:
                data: ChatGPTResponse | ChatGPTErrorResponse = await self._core.post(
                    token=token,
                    endpoint=ChatGPTEndpoint.PHOTO,
                    files=files,
                )

                if isinstance(data, ChatGPTErrorResponse):
                    last_error = data.error
                else:
                    return await self.__handle_success(
                        body,
                        data,
                    )

            except Exception as err:
                last_error = str(err)

            if attempt < max_attempts - 1:
                await sleep(1)

        return await self.__handle_failure(
            last_error,
            extra={"Токен авторизации": token},
        )

    async def toybox_to_photo(
        self,
        body: TB2PBody,
        image: UploadFile,
    ) -> ChatGPTResp:
        max_attempts = 10

        last_error = None

        data: IBody | PhotoGeneratorTemplates = (
            IBody(
                user_id=body.user_id,
                app_id=body.app_id,
                prompt=BODY_TOYBOX_PROMT.format(
                    box_color=body.box_color,
                    in_box=body.in_box,
                    box_name=body.box_name,
                ),
            )
            if body.box_color and body.in_box is not None
            else await templates_database.fetch_template("id", body.id, body.box_name)
        )

        files = await upload_chatgpt_file(
            data,
            image,
        )

        for attempt in range(max_attempts):
            token = conf.chatgpt_token
            try:
                data: ChatGPTResponse | ChatGPTErrorResponse = await self._core.post(
                    token=token,
                    endpoint=ChatGPTEndpoint.PHOTO,
                    files=files,
                )

                if isinstance(data, ChatGPTErrorResponse):
                    last_error = data.error
                else:
                    return await self.__handle_success(
                        body,
                        data,
                    )

            except Exception as err:
                last_error = str(err)

            if attempt < max_attempts - 1:
                await sleep(1)

        return await self.__handle_failure(
            last_error,
            extra={"Токен авторизации": token},
        )

    async def reshape_photo(
        self,
        body: R2PBody,
        image: UploadFile,
    ) -> ChatGPTResp:
        max_attempts = 10

        last_error = None

        body_prompt = R2PBodyPrompt.reshape(
            body.area,
            body.strength,
        )

        files = await upload_chatgpt_file(
            body_prompt,
            image,
        )

        for attempt in range(max_attempts):
            token = conf.chatgpt_token
            try:
                data = await self._core.post(
                    token=token,
                    endpoint=ChatGPTEndpoint.PHOTO,
                    files=files,
                )

                if isinstance(data, ChatGPTErrorResponse):
                    last_error = data.error
                else:
                    return await self.__handle_success(
                        body,
                        data,
                    )

            except Exception as err:
                last_error = str(err)

            if attempt < max_attempts - 1:
                await sleep(1)

        return await self.__handle_failure(
            last_error,
            extra={"Токен авторизации": token},
        )

    async def face_to_swap(
        self,
        body: I2CBody,
        images: list[UploadFile],  # Должно быть ровно 2 файла
    ) -> ChatGPTResp:
        if len(images) != 2:
            raise ValueError("Для face swap требуется ровно 2 изображения")

        max_attempts = 10
        last_error = None
        token = conf.chatgpt_token
        prompt = R2PBodyPrompt.face_swap().prompt

        # Объединяем два изображения в одно
        merged_bytes = await self._merge_two_images(images[0], images[1])

        # Формируем файлы для отправки
        files = [("image", ("face_swap.png", merged_bytes, "image/png"))]

        # Пытаемся отправить запрос несколько раз
        for attempt in range(max_attempts):
            try:
                data: ChatGPTResponse | ChatGPTErrorResponse = await self._core.post(
                    token=token,
                    endpoint=ChatGPTEndpoint.PHOTO,
                    data=IFaceSwapData(prompt=prompt),
                    files=files,
                )

                if isinstance(data, ChatGPTErrorResponse):
                    last_error = data.error
                else:
                    return await self.__handle_success(body, data)

            except Exception as err:
                last_error = str(err)

            # Пауза перед новой попыткой
            if attempt < max_attempts - 1:
                await sleep(1)

        # Если все попытки неудачны
        return await self.__handle_failure(
            last_error,
            extra={"Токен авторизации": token},
        )

    async def photo_to_antiques(
        self,
        image: UploadFile,
    ) -> Antiques:
        max_attempts = 1

        last_error = None

        ext = str(os.path.splitext(image.filename)[-1]).lower()
        image_bytes = await image.read()

        if ext in HEIF_EXTENSIONS:
            image_bytes, ext, _ = await convert_heic_to_jpg(
                image_bytes,
            )

        image_base64 = b64encode(image_bytes).decode("utf-8")

        for attempt in range(max_attempts):
            token = conf.chatgpt_token
            try:

                async def call(
                    token: str,
                ):
                    data = await self._core.post(
                        token=token,
                        is_response=False,
                        endpoint=ChatGPTEndpoint.CHAT,
                        body=AntiquesBody.create_image(
                            image_url=f"data:image/jpeg;base64,{image_base64}"
                        ),
                    )
                    return ChatGPTAntiquesResponse(**data)

                data = await call(token)

                if not isinstance(data, ChatGPTErrorResponse):
                    return data.fetch_data()

                last_error = data.error

            except Exception:
                if attempt == max_attempts - 1:
                    try:
                        data = await call(token)

                        if not data.error:
                            return data.fetch_data()

                    except Exception as final_err:
                        raise final_err
                    return await self.__handle_failure(last_error)
                await sleep(1)
        return await self.__handle_failure(
            last_error,
            extra={"Токен авторизации": token},
        )

    @staticmethod
    async def _merge_two_images(image1: UploadFile, image2: UploadFile) -> bytes:
        """Объединяем два изображения в одно для отправки в ChatGPT."""
        img1 = Image.open(BytesIO(await image1.read())).convert("RGBA")
        img2 = Image.open(BytesIO(await image2.read())).convert("RGBA")

        # Подгоняем размер второго изображения под первое
        img2 = img2.resize(img1.size)

        merged = Image.alpha_composite(img1, img2)

        buf = BytesIO()
        merged.save(buf, format="PNG")
        buf.seek(0)
        return buf.read()
