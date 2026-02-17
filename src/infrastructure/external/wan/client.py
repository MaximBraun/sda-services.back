# coding utf-8

from asyncio import sleep

from functools import reduce

from httpx import Response

from os import getenv

from fastapi import UploadFile

from .core import WanCore

from ....domain.conf import app_conf

from ....domain.errors import WanError

from ....domain.repositories import IDatabase

from ....domain.typing.enums import (
    WanEndpoint,
    WanMethod,
)

from ....domain.tools import (
    update_account_token,
)

from ....domain.entities.core import (
    IConfEnv,
)

from ....domain.entities.wan import (
    WanAuthBody,
    WanCookie,
    IT2IBody,
    IT2VBody,
    IE2VBody,
    IIT2IBody,
    IIT2VBody,
    IIG2MBody,
    IIF2PBody,
    IIF2UBody,
    III2VBody,
    IIE2VBody,
    II2IBody,
    IT2ABody,
    WanImageData,
)

from ...orm.database.repositories import (
    UserDataRepository,
    WanAccountRepository,
    WanAccountsTokensRepository,
    UserGenerationRepository,
    PhotoGeneratorTemplateRepository,
)

from ...orm.database.models import (
    WanAccounts,
    UserGenerations,
    PhotoGeneratorTemplates,
)

from ....interface.schemas.external import (
    WanResponse,
    IWanResponse,
    IWanPolicyData,
    GenerationData,
    IWanMediaResponse,
    UsrData,
)


conf: IConfEnv = app_conf()


wan_account_database = WanAccountRepository(
    engine=IDatabase(conf),
)


photo_generator_templates = PhotoGeneratorTemplateRepository(
    engine=IDatabase(conf),
)


wan_account_token_database = WanAccountsTokensRepository(
    engine=IDatabase(conf),
)


user_generations_database = UserGenerationRepository(
    engine=IDatabase(conf),
)

user_data_database = UserDataRepository(
    engine=IDatabase(conf),
)


class WanClient:
    def __init__(
        self,
        core: WanCore,
    ) -> None:
        self._core = core

    async def auth_user(
        self,
        account: WanAccounts,
    ) -> WanCookie:
        response: Response = await self._core.post(
            is_serialized=False,
            url_method=WanMethod.API,
            endpoint=WanEndpoint.AUTH,
            body=WanAuthBody(
                username=account.username,
                password=account.password,
            ),
        )
        return reduce(
            lambda _, cookie: WanCookie.model_validate(
                cookie,
            ),
            response.cookies.jar,
            None,
        )

    async def __fetch_account_cookie(
        self,
        account: WanAccounts,
    ) -> str:
        cookie: str | None = await wan_account_token_database.fetch_token(
            "account_id",
            account.id,
        )
        if cookie is None:
            account_cookie: WanCookie = await self.auth_user(account)

            cookie: str = account_cookie.generate_cookie()

            await update_account_token(
                account,
                project="wan",
                cookies=cookie,
            )

        return cookie

    async def __handle_success(
        self,
        data: WanResponse,
        account_id: int,
        user_id: str,
        app_id: str,
    ) -> IWanResponse:
        await user_generations_database.add_record(
            GenerationData(
                generation_id=data.data,
                account_id=account_id,
                user_id=user_id,
                app_id=app_id,
                app_name=getenv("APP_SERVICE", "wan").lower(),
            )
        )
        await user_data_database.create_or_update_user_data(
            UsrData(
                user_id=user_id,
                app_id=app_id,
            )
        )
        return IWanResponse(
            media_id=data.data,
        )

    async def __handle_failure(
        self,
        status_code: int,
        extra: dict[str] = {},
    ) -> WanError:
        error = WanError(
            status_code=9999 if status_code is None else status_code,
            extra=extra,
        )

        raise error

    async def __reauthenticate(
        self,
        account: WanAccounts,
    ) -> WanCookie:
        return await self.auth_user(
            account,
        )

    async def __upload_file(
        self,
        cookie: str,
        data: IWanPolicyData,
        image: UploadFile,
    ) -> Response:
        iamge_bytes: bytes = await image.read()

        return await self._core.post(
            cookie=cookie,
            is_serialized=False,
            url_method=WanMethod.OSS,
            data=IIF2UBody(**data.dict),
            files={
                "file": (image.filename, iamge_bytes, image.content_type),
            },
        )

    async def __fetch_policy(
        self,
        cookie: str,
        image: UploadFile,
    ) -> IWanPolicyData:
        data: WanResponse = await self._core.post(
            cookie=cookie,
            url_method=WanMethod.API,
            endpoint=WanEndpoint.POLICY,
            body=IIF2PBody(
                file_name=image.filename,
            ),
        )
        if data.error_code == 0:
            return data.data
        raise WanError(data.error_code)

    async def __generate_oss_url(
        self,
        cookie: str,
        data: IWanPolicyData,
    ) -> str:
        data: WanResponse = await self._core.post(
            cookie=cookie,
            url_method=WanMethod.API,
            endpoint=WanEndpoint.OSS,
            body=IIF2PBody(
                key=data.key,
            ),
        )
        if data.error_code == 0:
            return data.data
        raise WanError(data.error_code)

    async def text_to_image(
        self,
        body: IT2IBody,
        user_id: str,
        app_id: str,
    ) -> IWanResponse:
        account: WanAccounts | None = await wan_account_database.fetch_next_account(
            app_id,
        )

        if account is None:
            raise WanError(status_code=5005)

        account_id = account.id

        max_attempts = 10

        last_err_code = None

        for attempt in range(max_attempts):
            cookie: str = await self.__fetch_account_cookie(
                account,
            )
            try:

                async def call(
                    cookie: str,
                ) -> WanResponse:
                    return await self._core.post(
                        cookie=cookie,
                        url_method=WanMethod.API,
                        endpoint=WanEndpoint.GENERATION,
                        body=IIT2IBody.generate(
                            prompt=body.prompt,
                            model_version="2_1_turbo",
                        ),
                    )

                data: WanResponse = await call(
                    cookie,
                )

                if data.error_code == 0:
                    return await self.__handle_success(
                        data,
                        account_id,
                        user_id,
                        app_id,
                    )

                elif data.error_code == 4009:
                    raise WanError(data.error_code)

                last_err_code = data.error_code

            except Exception:
                if attempt == max_attempts - 1:
                    account_cookie: WanCookie = await self.__reauthenticate(
                        account,
                    )

                    cookie: str = account_cookie.generate_cookie()

                    await update_account_token(
                        account,
                        cookies=cookie,
                        project="wan",
                    )

                    try:
                        data = await call(
                            cookie,
                        )

                        if data.error_code == 0:
                            return await self.__handle_success(
                                data,
                                account_id,
                                user_id,
                                app_id,
                            )
                    except Exception as final_err:
                        raise final_err
                    return await self.__handle_failure(data.error_code)
                await sleep(1)

        return await self.__handle_failure(
            last_err_code,
            extra={
                "Данные аккаунта": {
                    "логин": account.username,
                    "пароль": account.password,
                }
            },
        )

    async def photo_to_photo(
        self,
        body: IT2IBody,
        image: UploadFile,
        user_id: str,
        app_id: str,
    ):
        account: WanAccounts | None = await wan_account_database.fetch_next_account(
            app_id,
        )

        if account is None:
            raise WanError(status_code=5005)

        account_id = account.id

        max_attempts = 10

        last_err_code = None

        for attempt in range(max_attempts):
            cookie: str = await self.__fetch_account_cookie(
                account,
            )
            try:

                async def call(
                    cookie: str,
                ) -> WanResponse:
                    policy_data: IWanPolicyData = await self.__fetch_policy(
                        cookie=cookie,
                        image=image,
                    )

                    await self.__upload_file(
                        cookie=cookie,
                        data=policy_data,
                        image=image,
                    )

                    oss_url: str = await self.__generate_oss_url(
                        cookie=cookie,
                        data=policy_data,
                    )

                    return await self._core.post(
                        cookie=cookie,
                        url_method=WanMethod.API,
                        endpoint=WanEndpoint.GENERATION,
                        body=II2IBody.generate(
                            prompt=body.prompt,
                            ref_images_url_info=[
                                WanImageData(
                                    name=image.filename,
                                    origin_image=oss_url,
                                    result_image=oss_url,
                                )
                            ],
                            generation_mode="plain",
                            sub_type="chat",
                        ),
                    )

                data: WanResponse = await call(
                    cookie,
                )

                if data.error_code == 0:
                    return await self.__handle_success(
                        data,
                        account_id,
                        user_id,
                        app_id,
                    )

                elif data.error_code == 4009:
                    raise WanError(data.error_code)

                last_err_code = data.error_code

            except Exception:
                if attempt == max_attempts - 1:
                    account_cookie: WanCookie = await self.__reauthenticate(
                        account,
                    )

                    cookie: str = account_cookie.generate_cookie()

                    await update_account_token(
                        account,
                        cookies=cookie,
                        project="wan",
                    )

                    try:
                        data = await call(
                            cookie,
                        )

                        if data.error_code == 0:
                            return await self.__handle_success(
                                data,
                                account_id,
                                user_id,
                                app_id,
                            )
                    except Exception as final_err:
                        raise final_err
                    return await self.__handle_failure(data.error_code)
                await sleep(1)

        return await self.__handle_failure(
            last_err_code,
            extra={
                "Данные аккаунта": {
                    "логин": account.username,
                    "пароль": account.password,
                }
            },
        )

    async def template_to_photo(
        self,
        id: int,
        image: UploadFile,
        user_id: str,
        app_id: str,
    ):
        account: WanAccounts | None = await wan_account_database.fetch_next_account(
            app_id,
        )

        if account is None:
            raise WanError(status_code=5005)

        account_id = account.id

        max_attempts = 10

        last_err_code = None

        for attempt in range(max_attempts):
            cookie: str = await self.__fetch_account_cookie(
                account,
            )
            try:

                async def call(
                    cookie: str,
                ) -> WanResponse:
                    template: PhotoGeneratorTemplates = (
                        await photo_generator_templates.fetch_with_filters(
                            id=id,
                        )
                    )

                    policy_data: IWanPolicyData = await self.__fetch_policy(
                        cookie=cookie,
                        image=image,
                    )

                    await self.__upload_file(
                        cookie=cookie,
                        data=policy_data,
                        image=image,
                    )

                    oss_url: str = await self.__generate_oss_url(
                        cookie=cookie,
                        data=policy_data,
                    )

                    return await self._core.post(
                        cookie=cookie,
                        url_method=WanMethod.API,
                        endpoint=WanEndpoint.GENERATION,
                        body=II2IBody.generate(
                            prompt=template.prompt,
                            ref_images_url_info=[
                                WanImageData(
                                    name=image.filename,
                                    origin_image=oss_url,
                                    result_image=oss_url,
                                )
                            ],
                            generation_mode="plain",
                            sub_type="chat",
                        ),
                    )

                data: WanResponse = await call(
                    cookie,
                )

                if data.error_code == 0:
                    return await self.__handle_success(
                        data,
                        account_id,
                        user_id,
                        app_id,
                    )

                elif data.error_code == 4009:
                    raise WanError(data.error_code)

                last_err_code = data.error_code

            except Exception:
                if attempt == max_attempts - 1:
                    account_cookie: WanCookie = await self.__reauthenticate(
                        account,
                    )

                    cookie: str = account_cookie.generate_cookie()

                    await update_account_token(
                        account,
                        cookies=cookie,
                        project="wan",
                    )

                    try:
                        data = await call(
                            cookie,
                        )

                        if data.error_code == 0:
                            return await self.__handle_success(
                                data,
                                account_id,
                                user_id,
                                app_id,
                            )
                    except Exception as final_err:
                        raise final_err
                    return await self.__handle_failure(data.error_code)
                await sleep(1)

        return await self.__handle_failure(
            last_err_code,
            extra={
                "Данные аккаунта": {
                    "логин": account.username,
                    "пароль": account.password,
                }
            },
        )

    async def template_to_avatar(
        self,
        id: int,
        body: IT2ABody,
        image: UploadFile,
        user_id: str,
        app_id: str,
    ):
        account: WanAccounts | None = await wan_account_database.fetch_next_account(
            app_id,
        )

        if account is None:
            raise WanError(status_code=5005)

        account_id = account.id

        max_attempts = 10

        last_err_code = None

        for attempt in range(max_attempts):
            cookie: str = await self.__fetch_account_cookie(
                account,
            )
            try:

                async def call(
                    cookie: str,
                ) -> WanResponse:
                    template: PhotoGeneratorTemplates = (
                        await photo_generator_templates.fetch_with_filters(
                            id=id,
                        )
                    )

                    prompt = (
                        template.prompt
                        + "\n"
                        + "Create a high-quality user avatar based on the provided image. "
                        f"Apply the selected camera angle: {body.angle}. "
                        f"Use the described pose: {body.pose}. "
                        "Ensure the avatar looks natural, consistent with the user's appearance, "
                        "and rendered in the same visual style specified by the template."
                    )

                    policy_data: IWanPolicyData = await self.__fetch_policy(
                        cookie=cookie,
                        image=image,
                    )

                    await self.__upload_file(
                        cookie=cookie,
                        data=policy_data,
                        image=image,
                    )

                    oss_url: str = await self.__generate_oss_url(
                        cookie=cookie,
                        data=policy_data,
                    )

                    return await self._core.post(
                        cookie=cookie,
                        url_method=WanMethod.API,
                        endpoint=WanEndpoint.GENERATION,
                        body=II2IBody.generate(
                            prompt=prompt,
                            ref_images_url_info=[
                                WanImageData(
                                    name=image.filename,
                                    origin_image=oss_url,
                                    result_image=oss_url,
                                )
                            ],
                            generation_mode="plain",
                            sub_type="chat",
                        ),
                    )

                data: WanResponse = await call(
                    cookie,
                )

                if data.error_code == 0:
                    return await self.__handle_success(
                        data,
                        account_id,
                        user_id,
                        app_id,
                    )

                elif data.error_code == 4009:
                    raise WanError(data.error_code)

                last_err_code = data.error_code

            except Exception:
                if attempt == max_attempts - 1:
                    account_cookie: WanCookie = await self.__reauthenticate(
                        account,
                    )

                    cookie: str = account_cookie.generate_cookie()

                    await update_account_token(
                        account,
                        cookies=cookie,
                        project="wan",
                    )

                    try:
                        data = await call(
                            cookie,
                        )

                        if data.error_code == 0:
                            return await self.__handle_success(
                                data,
                                account_id,
                                user_id,
                                app_id,
                            )
                    except Exception as final_err:
                        raise final_err
                    return await self.__handle_failure(data.error_code)
                await sleep(1)

        return await self.__handle_failure(
            last_err_code,
            extra={
                "Данные аккаунта": {
                    "логин": account.username,
                    "пароль": account.password,
                }
            },
        )

    async def text_to_video(
        self,
        body: IT2VBody,
        user_id: str,
        app_id: str,
    ) -> IWanResponse:
        account: WanAccounts | None = await wan_account_database.fetch_next_account(
            app_id,
        )

        if account is None:
            raise WanError(status_code=5005)

        account_id = account.id

        max_attempts = 10

        last_err_code = None

        for attempt in range(max_attempts):
            cookie: str = await self.__fetch_account_cookie(
                account,
            )
            try:

                async def call(
                    cookie: str,
                ) -> WanResponse:
                    return await self._core.post(
                        cookie=cookie,
                        url_method=WanMethod.API,
                        endpoint=WanEndpoint.GENERATION,
                        body=IIT2VBody.generate(
                            prompt=body.prompt,
                            duration=5,
                            video_sound_switch="on",
                            resolution="1280*720",
                        ),
                    )

                data: WanResponse = await call(
                    cookie,
                )

                if data.error_code == 0:
                    return await self.__handle_success(
                        data,
                        account_id,
                        user_id,
                        app_id,
                    )

                elif data.error_code == 4009:
                    raise WanError(data.error_code)

                last_err_code = data.error_code

            except Exception:
                if attempt == max_attempts - 1:
                    account_cookie: WanCookie = await self.__reauthenticate(
                        account,
                    )

                    cookie: str = account_cookie.generate_cookie()

                    await update_account_token(
                        account,
                        cookies=cookie,
                        project="wan",
                    )

                    try:
                        data = await call(
                            cookie,
                        )

                        if data.error_code == 0:
                            return await self.__handle_success(
                                data,
                                account_id,
                                user_id,
                                app_id,
                            )
                    except Exception as final_err:
                        raise final_err
                    return await self.__handle_failure(data.error_code)
                await sleep(1)

        return await self.__handle_failure(
            last_err_code,
            extra={
                "Данные аккаунта": {
                    "логин": account.username,
                    "пароль": account.password,
                }
            },
        )

    async def image_to_video(
        self,
        image: UploadFile,
        body: IT2VBody,
        user_id: str,
        app_id: str,
    ) -> IWanResponse:
        account: WanAccounts | None = await wan_account_database.fetch_next_account(
            app_id,
        )

        if account is None:
            raise WanError(status_code=5005)

        account_id = account.id

        max_attempts = 10

        last_err_code = None

        for attempt in range(max_attempts):
            cookie: str = await self.__fetch_account_cookie(
                account,
            )
            try:

                async def call(
                    cookie: str,
                ) -> WanResponse:
                    policy_data: IWanPolicyData = await self.__fetch_policy(
                        cookie=cookie,
                        image=image,
                    )

                    await self.__upload_file(
                        cookie=cookie,
                        data=policy_data,
                        image=image,
                    )

                    oss_url: str = await self.__generate_oss_url(
                        cookie=cookie,
                        data=policy_data,
                    )

                    return await self._core.post(
                        cookie=cookie,
                        url_method=WanMethod.API,
                        endpoint=WanEndpoint.GENERATION,
                        body=III2VBody.generate(
                            prompt=body.prompt,
                            duration=5,
                            base_image=oss_url,
                            video_sound_switch="on",
                            resolution="1280*720",
                        ),
                    )

                data: WanResponse = await call(
                    cookie,
                )

                if data.error_code == 0:
                    return await self.__handle_success(
                        data,
                        account_id,
                        user_id,
                        app_id,
                    )

                elif data.error_code == 4009:
                    raise WanError(data.error_code)

                last_err_code = data.error_code

            except Exception:
                if attempt == max_attempts - 1:
                    account_cookie: WanCookie = await self.__reauthenticate(
                        account,
                    )

                    cookie: str = account_cookie.generate_cookie()

                    await update_account_token(
                        account,
                        cookies=cookie,
                        project="wan",
                    )

                    try:
                        data = await call(
                            cookie,
                        )

                        if data.error_code == 0:
                            return await self.__handle_success(
                                data,
                                account_id,
                                user_id,
                                app_id,
                            )
                    except Exception as final_err:
                        raise final_err
                    return await self.__handle_failure(data.error_code)
                await sleep(1)

        return await self.__handle_failure(
            last_err_code,
            extra={
                "Данные аккаунта": {
                    "логин": account.username,
                    "пароль": account.password,
                }
            },
        )

    async def template_to_video(
        self,
        image: UploadFile,
        body: IE2VBody,
        user_id: str,
        app_id: str,
    ) -> IWanResponse:
        account: WanAccounts | None = await wan_account_database.fetch_next_account(
            app_id,
        )

        if account is None:
            raise WanError(status_code=5005)

        account_id = account.id

        max_attempts = 10

        last_err_code = None

        for attempt in range(max_attempts):
            cookie: str = await self.__fetch_account_cookie(
                account,
            )
            try:

                async def call(
                    cookie: str,
                ) -> WanResponse:
                    policy_data: IWanPolicyData = await self.__fetch_policy(
                        cookie=cookie,
                        image=image,
                    )

                    await self.__upload_file(
                        cookie=cookie,
                        data=policy_data,
                        image=image,
                    )

                    oss_url: str = await self.__generate_oss_url(
                        cookie=cookie,
                        data=policy_data,
                    )

                    return await self._core.post(
                        cookie=cookie,
                        url_method=WanMethod.API,
                        endpoint=WanEndpoint.GENERATION,
                        body=IIE2VBody.generate(
                            base_image=oss_url,
                            video_sound_switch="off",
                            model_version="2_2",
                            model_ids=[
                                body.template_id,
                            ],
                        ),
                    )

                data: WanResponse = await call(
                    cookie,
                )

                if data.error_code == 0:
                    return await self.__handle_success(
                        data,
                        account_id,
                        user_id,
                        app_id,
                    )

                elif data.error_code == 4009:
                    raise WanError(data.error_code)

                last_err_code = data.error_code

            except Exception:
                if attempt == max_attempts - 1:
                    account_cookie: WanCookie = await self.__reauthenticate(
                        account,
                    )

                    cookie: str = account_cookie.generate_cookie()

                    await update_account_token(
                        account,
                        cookies=cookie,
                        project="wan",
                    )

                    try:
                        data = await call(
                            cookie,
                        )

                        if data.error_code == 0:
                            return await self.__handle_success(
                                data,
                                account_id,
                                user_id,
                                app_id,
                            )
                    except Exception as final_err:
                        raise final_err
                    return await self.__handle_failure(data.error_code)
                await sleep(1)

        return await self.__handle_failure(
            last_err_code,
            extra={
                "Данные аккаунта": {
                    "логин": account.username,
                    "пароль": account.password,
                }
            },
        )

    async def fetch_media_status(
        self,
        id: str,
    ) -> IWanMediaResponse:
        generation_data: (
            UserGenerations | None
        ) = await user_generations_database.fetch_generation(
            "generation_id",
            id,
        )

        if generation_data is None:
            raise WanError(status_code=6005)

        account: WanAccounts | None = await wan_account_database.fetch_account(
            "id",
            generation_data.account_id,
        )

        max_attempts = 1

        last_err_code = None

        for attempt in range(max_attempts):
            cookie: str = await self.__fetch_account_cookie(
                account,
            )
            try:

                async def call(
                    cookie: str,
                    id: str,
                ) -> WanResponse:
                    return await self._core.post(
                        cookie=cookie,
                        url_method=WanMethod.API,
                        endpoint=WanEndpoint.STATUS,
                        body=IIG2MBody(
                            task_id=id,
                        ),
                    )

                data: WanResponse = await call(
                    cookie,
                    id,
                )

                if data.error_code == 0:
                    return IWanMediaResponse.from_data(
                        data,
                    )

                elif data.error_code == 10002:
                    raise WanError(data.error_code)

                last_err_code: int = data.error_code

            except Exception:
                if attempt == max_attempts - 1:
                    account_cookie = await self.__reauthenticate(
                        account,
                    )

                    cookie: str = account_cookie.generate_cookie()

                    await update_account_token(
                        account,
                        cookies=cookie,
                        project="wan",
                    )

                    try:
                        data = await call(
                            cookie,
                            id,
                        )

                        if data.error_code == 0:
                            return IWanMediaResponse.from_data(
                                data,
                            )

                    except Exception as final_err:
                        raise final_err
                    return await self.__handle_failure(data.error_code)
                await sleep(1)

        return await self.__handle_failure(
            last_err_code,
            extra={
                "Данные аккаунта": {
                    "логин": account.username,
                    "пароль": account.password,
                }
            },
        )
