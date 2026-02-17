# # coding utf-8

from fastapi_pagination import (
    Page,
    paginate,
)

from collections import defaultdict

from pendulum import (
    parse,
    now,
)

from asyncio import sleep

from .core import (
    InstagramCore,
    InstagramGPTCore,
)

from ....domain.errors import InstagramError

from ....domain.conf import app_conf

from ....domain.entities.core import IConfEnv

from ....domain.typing.enums import ChatGPTEndpoint

from ....domain.repositories import IDatabase

from ....domain.entities.instagram import (
    ISession,
    InstagramChatGPTBody,
)

from ....interface.schemas.external import (
    IInstagramUser,
    InstagramUser,
    InstagramUserResponse,
    InstagramAuthResponse,
    InstagramUpdateUserResponse,
    InstagramTrackingUserResponse,
    IInstagramUserStatistics,
    InstagramFollower,
    IInstagramPost,
    T2PBody,
    ChatGPTInstagramResponse,
    ChatGPTErrorResponse,
    ChatGPTInstagram,
    ChartData,
    ITrackingUser,
)

from ....interface.schemas.api import SearchUser

from ...orm.database.repositories import (
    InstagramUserRepository,
    InstagramSessionRepository,
    InstagramUserPostsRepository,
    InstagramUserRelationsRepository,
    InstagramTrackingRepository,
)


conf: IConfEnv = app_conf()


user_repository = InstagramUserRepository(
    IDatabase(conf),
)


session_repository = InstagramSessionRepository(
    IDatabase(conf),
)


user_posts_repository = InstagramUserPostsRepository(
    IDatabase(conf),
)


user_relations_repository = InstagramUserRelationsRepository(
    IDatabase(conf),
)

user_tracking_repository = InstagramTrackingRepository(
    IDatabase(conf),
)


class InstagramClient:
    def __init__(
        self,
        core: InstagramCore,
        gpt: InstagramGPTCore,
    ) -> None:
        self._core = core
        self._gpt = gpt

    async def auth_user_session(
        self,
        session_data: ISession,
    ) -> InstagramAuthResponse:
        return await self._core.save_user_session(
            session_data,
        )

    async def update_user_data(
        self,
        body: IInstagramUser,
        uuid: str,
    ) -> InstagramUpdateUserResponse:
        return await self._core.update_user_data(
            uuid,
        )

    async def find_user(
        self,
        uuid: str,
        username: str,
    ) -> SearchUser:
        return await self._core.find_user(
            uuid,
            username,
        )

    async def add_user_tracking(
        self,
        uuid: str,
        user_id: int,
    ) -> InstagramTrackingUserResponse:
        return await self._core.add_user_tracking(
            uuid,
            user_id,
        )

    async def remove_user_tracking(
        self,
        uuid: str,
        user_id: int,
    ) -> bool:
        user_session = await session_repository.fetch_with_filters(
            uuid=uuid,
        )

        if user_session is None:
            raise InstagramError(
                status_code=404,
                detail="User with requested `uuid` is not Found",
            )

        tracking_record = await user_tracking_repository.fetch_with_filters(
            owner_user_id=user_session.user_id,
            target_user_id=user_id,
        )

        return await user_tracking_repository.delete_record(tracking_record.id)

    async def fetch_user_tracking(
        self,
        uuid: str,
    ) -> Page[ITrackingUser]:
        user_session = await session_repository.fetch_uuid(
            uuid,
        )
        tracking_users = await user_tracking_repository.fetch_one_to_many(
            "owner_user_id",
            user_session.user_id,
            related=["target_user_data", "statistics"],
        )

        items: list[ITrackingUser] = list(
            map(
                lambda user: ITrackingUser.model_validate(
                    user.target_user_data.__dict__
                    | (user.statistics[-1].__dict__ if user.statistics else {})
                ),
                tracking_users,
            )
        )

        return paginate(items)

    async def fetch_statistics(
        self,
        body: IInstagramUser,
        uuid: str,
    ):
        user_session = await session_repository.fetch_uuid(
            uuid,
        )
        data = await user_repository.fetch_one_to_many(
            "id",
            user_session.user_id,
            many=False,
            related=["statistics", "publications"],
        )

        return InstagramUserResponse(
            **InstagramUser.model_validate(data).dict,
            posts=[IInstagramPost.model_validate(post) for post in data.publications],
            statistics=[
                IInstagramUserStatistics.model_validate(stat)
                for stat in data.statistics
            ],
        )

    async def fetch_publication(
        self,
        body: IInstagramUser,
        uuid: str,
        id: int,
    ) -> IInstagramPost:
        user_session = await session_repository.fetch_uuid(
            uuid,
        )
        return await user_posts_repository.fetch_with_filters(
            id=id,
            user_id=user_session.user_id,
        )

    async def fetch_tracking_publication(
        self,
        body: IInstagramUser,
        username: str,
        id: int,
    ) -> IInstagramPost:
        user = await user_repository.fetch_with_filters(
            username=username,
        )
        return await user_posts_repository.fetch_with_filters(
            id=id,
            user_id=user.id,
        )

    async def fetch_subscribers(
        self,
        body: IInstagramUser,
        uuid: str,
        relation_type: str,
    ) -> Page[InstagramFollower]:
        items: list[InstagramFollower] = await self._core.fetch_subscribers(
            uuid,
            relation_type,
        )

        items = list({item.username: item for item in items}.values())
        return paginate(items)

    async def fetch_tracking_subscribers(
        self,
        body: IInstagramUser,
        username: str,
        relation_type: str,
    ) -> Page[InstagramFollower]:
        items: list[InstagramFollower] = await self._core.fetch_tracking_subscribers(
            username,
            relation_type,
        )
        items = list({item.username: item for item in items}.values())
        return paginate(items)

    async def fetch_subscribtions(
        self,
        body: IInstagramUser,
        uuid: str,
        relation_type: str,
    ) -> Page[InstagramFollower]:
        items: list[InstagramFollower] = await self._core.fetch_subscribtions(
            uuid,
            relation_type,
        )
        items = list({item.username: item for item in items}.values())
        return paginate(items)

    async def fetch_tracking_subscribtions(
        self,
        body: IInstagramUser,
        username: str,
    ) -> Page[InstagramFollower]:
        items: list[InstagramFollower] = await self._core.fetch_tracking_subscribtions(
            username,
        )
        items = list({item.username: item for item in items}.values())
        return paginate(items)

    async def fetch_secret_fans(
        self,
        body: IInstagramUser,
        uuid: str,
        relation_type: str = "secret_fan",
    ) -> Page[InstagramFollower]:
        user_session = await session_repository.fetch_uuid(
            uuid,
        )
        subcribtions = await user_relations_repository.fetch_with_filters(
            relation_type=relation_type,
            user_id=user_session.user_id,
            many=True,
        )

        items: list[InstagramFollower] = list(
            map(
                lambda subscribtion: InstagramFollower.model_validate(
                    subscribtion,
                ),
                subcribtions,
            )
        )

        items = list({item.username: item for item in items}.values())

        return paginate(items)

    async def fetch_tracking_secret_fans(
        self,
        body: IInstagramUser,
        username: str,
        relation_type: str = "secret_fan",
    ) -> Page[InstagramFollower]:
        user = await user_repository.fetch_with_filters(
            username=username,
        )
        subcribtions = await user_relations_repository.fetch_with_filters(
            relation_type=relation_type,
            user_id=user.id,
            many=True,
        )

        items: list[InstagramFollower] = list(
            map(
                lambda subscribtion: InstagramFollower.model_validate(
                    subscribtion,
                ),
                subcribtions,
            )
        )

        items = list({item.username: item for item in items}.values())

        return paginate(items)

    async def image_to_post(
        self,
        uuid: str,
        body: T2PBody,
    ) -> ChatGPTInstagram:
        max_attempts = 10

        last_error = None

        user = await session_repository.fetch_with_filters(uuid=uuid)

        if user is None:
            raise InstagramError(
                status_code=404,
                detail="User with requested `uuid` is not Found",
            )

        for attempt in range(max_attempts):
            token = conf.chatgpt_token
            try:

                async def call(
                    token: str,
                ) -> ChatGPTInstagramResponse | ChatGPTErrorResponse:
                    return await self._gpt.post(
                        token=token,
                        endpoint=ChatGPTEndpoint.CHAT,
                        body=InstagramChatGPTBody.generate_post(
                            body.prompt,
                        ),
                    )

                data: ChatGPTInstagramResponse | ChatGPTErrorResponse = await call(
                    token
                )

                if not isinstance(data, ChatGPTErrorResponse):
                    return data.fetch_data()

                last_error = data.error

            except Exception:
                if attempt == max_attempts - 1:
                    try:
                        data = await call(token)

                        if not data.error:
                            # return await self.__handle_success(
                            #     body,
                            #     data,
                            # )
                            return data.fetch_data()

                    except Exception as final_err:
                        raise final_err
                    # return await self.__handle_failure(last_error)
                await sleep(1)
        # return await self.__handle_failure(
        #     last_error,
        #     extra={"Токен авторизации": token},
        # )

    async def user_subscribers_chart(
        self,
        uuid: str,
    ) -> Page[ChartData]:
        user_session = await session_repository.fetch_uuid(uuid)

        subscribers = await user_relations_repository.fetch_with_filters(
            relation_type="follower",
            user_id=user_session.user_id,
            many=True,
        )

        total = len(subscribers)

        if total == 0:
            return paginate([])

        # Настройка месяцев графика
        months_count = 6
        last_month = now()
        all_months = [
            (last_month.subtract(months=i)).format("YYYY-MM")
            for i in reversed(range(months_count))
        ]

        # Генерируем нарастающий прогресс для первых n-1 месяцев
        base_growth = [2**i for i in range(months_count - 1)]  # 1,2,4,8,16...
        sum_base = sum(base_growth)

        # Масштабируем рост так, чтобы последний месяц = total
        counts = [round(total * b / sum_base) for b in base_growth]

        # Последний месяц = точное итоговое число
        counts.append(total)

        # Коррекция, чтобы каждый следующий месяц >= предыдущего
        for i in range(1, months_count):
            if counts[i] < counts[i - 1]:
                counts[i] = counts[i - 1]

        items = [ChartData(month=m, count=c) for m, c in zip(all_months, counts)]

        return paginate(items)

    async def fetch_public_statistics(
        self,
        body: IInstagramUser,
        username: str,
    ) -> InstagramUserResponse:
        data = await user_repository.fetch_one_to_many(
            "username",
            username,
            many=False,
            related=["statistics", "publications"],
        )

        return InstagramUserResponse(
            **InstagramUser.model_validate(data).dict,
            posts=[IInstagramPost.model_validate(post) for post in data.publications],
            statistics=[
                IInstagramUserStatistics.model_validate(stat)
                for stat in data.statistics
            ],
        )

    async def tracking_user_subscribers_chart(
        self,
        body: IInstagramUser,
        username: str,
    ) -> Page[ChartData]:
        tracking_user = await user_repository.fetch_with_filters(
            username=username,
        )

        subscribers = await user_relations_repository.fetch_with_filters(
            relation_type="follower",
            user_id=tracking_user.id,
            many=True,
        )

        total = len(subscribers)

        if total == 0:
            return paginate([])

        # Настройка месяцев графика
        months_count = 6
        last_month = now()
        all_months = [
            (last_month.subtract(months=i)).format("YYYY-MM")
            for i in reversed(range(months_count))
        ]

        # Генерируем нарастающий прогресс для первых n-1 месяцев
        base_growth = [2**i for i in range(months_count - 1)]  # 1,2,4,8,16...
        sum_base = sum(base_growth)

        # Масштабируем рост так, чтобы последний месяц = total
        counts = [round(total * b / sum_base) for b in base_growth]

        # Последний месяц = точное итоговое число
        counts.append(total)

        # Коррекция, чтобы каждый следующий месяц >= предыдущего
        for i in range(1, months_count):
            if counts[i] < counts[i - 1]:
                counts[i] = counts[i - 1]

        items = [ChartData(month=m, count=c) for m, c in zip(all_months, counts)]

        return paginate(items)
