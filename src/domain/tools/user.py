# coding utf-8

from typing import Any

from ..conf import app_conf

from functools import wraps

from fastapi import Request

from fastapi.responses import JSONResponse

from .message import format_message

from ..entities.core import (
    IConfEnv,
    IWebhook,
    ISchema,
)

from ..entities.bot import IBotReporter

from ..errors import PixverseError

from ...interface.schemas.external import (
    UserUpdateData,
    UserEventData,
)

from ...interface.schemas.external.body import IPixverseBody, ITopmediaBody

from ..repositories import IDatabase

from ...infrastructure.orm.database.repositories import (
    UserDataRepository,
    ApplicationRepository,
    UserEventRepository,
)


conf: IConfEnv = app_conf()


telegram_bot = IBotReporter(
    conf,
)

conf: IConfEnv = app_conf()


user_repository = UserDataRepository(
    IDatabase(conf),
)

user_event_repository = UserEventRepository(
    IDatabase(conf),
)

application_repository = ApplicationRepository(
    IDatabase(conf),
)


async def add_user_tokens(
    data: IWebhook,
) -> ISchema:
    application_data: (
        Any | None
    ) = await application_repository.fetch_application_by_bundle_id(
        "application_id",
        data.app.bundle_id,
        ["products"],
    )

    if application_data is None:
        return None

    matched_product = next(
        (
            product
            for product in application_data.products
            if product.name == data.event.properties.product_id
        ),
        None,
    )

    if matched_product is None:
        return None

    user = await user_repository.fetch_with_filters(
        user_id=data.user.user_id,
        app_id=data.app.bundle_id,
    )

    actual_user = user or data.user

    user_data = UserUpdateData(
        user_id=actual_user.user_id,
        app_id=actual_user.app_id if user else data.app.bundle_id,
        balance=int((user.balance if user else 0) + matched_product.tokens_amount),
        app_id_usage=user.app_id_usage if user else 1,
    )

    user_event_data = UserEventData(
        name=data.event.name,
        user_id=data.user.user_id,
        app_id=data.app.bundle_id,
        product_id=data.event.properties.product_id,
    )

    await user_event_repository.add_record(
        user_event_data,
    )

    message = format_message(
        title="Произошла оплата",
        fields={
            "👤 Пользователь:": data.user.user_id,
            "📱 Приложение:": data.app.bundle_id,
            "🛒 Продукт:": data.event.properties.product_id,
        },
    )

    await telegram_bot.send_error_message(
        text=message,
    )

    return await user_repository.create_or_update_user_data(
        user_data,
    )


def check_user_tokens(method_cost: int):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request: Request = kwargs.get("request")
            if request is None:
                for arg in args:
                    if isinstance(arg, Request):
                        request = arg
                        break

            if request is None:
                return JSONResponse(
                    status_code=400,
                    content={"detail": "Request object not found"},
                )

            try:
                body = dict(
                    pair.split("=", 1)
                    for pair in str(request.query_params).split("&")
                    if pair
                )

                if body.get("app_bundle_id"):
                    data = ITopmediaBody(**body)
                else:
                    data = IPixverseBody(**body)

            except Exception as e:
                return JSONResponse(
                    status_code=422,
                    content={"detail": f"Invalid request body: {e}"},
                )

            applications = await application_repository.fetch_with_filters(
                available_tokens=1,
                many=True,
            )

            user = None
            if applications and data.app_id in {
                app.application_id for app in applications
            }:
                user = await user_repository.fetch_with_filters(
                    user_id=data.user_id,
                    app_id=data.app_id,
                )

                if user is None or user.balance < method_cost:
                    raise PixverseError(
                        402,
                        extra={
                            "Информация о пользователе": f"{data.user_id}\n\n{data.app_id}"
                        },
                    )

            result = await func(*args, **kwargs)

            if user:
                user_data = UserUpdateData(
                    user_id=data.user_id,
                    app_id=data.app_id,
                    balance=user.balance - method_cost,
                    app_id_usage=user.app_id_usage + 1,
                )

                await user_repository.create_or_update_user_data(user_data)

            return result

        return wrapper

    return decorator
