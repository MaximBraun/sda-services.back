# coding: utf-8

from typing import (
    Any,
    Callable,
    Generator,
)

from datetime import date

from inspect import signature

from uuid import uuid4

from pendulum import now

from functools import wraps

from rocketapi import InstagramAPI

from rocketapi.exceptions import BadResponseException

from instaloader import (
    ProfileNotExistsException,
    TooManyRequestsException,
)

from httpx import HTTPError

from fastapi import HTTPException

from ..core import HttpClient

from ....domain.entities.core import IConfEnv

from ....domain.conf import app_conf

from ....domain.errors import InstagramError

from ....domain.constants import CHATGPT_API_URL
from ....domain.entities.instagram import ISession
from ....domain.entities.chatgpt import IAuthHeaders
from ....domain.typing.enums import RequestMethod
from ....domain.repositories.engines.database import IDatabase

from ....interface.schemas.api import (
    AddSession,
    IUser,
    SearchUser,
    UserTracking,
    RocketBodyUser,
    IRocketBodyUser,
    RocketBodyMedia,
)
from ....interface.schemas.external import (
    InstagramUserStatistics,
    InstagramPost,
    UserRelationStats,
    InstagramFollower,
    ChatGPTErrorResponse,
    ChatGPTInstagramResponse,
    RocketProfile,
    IRocketProfile,
    InstagramAuthResponse,
    InstagramUpdateUserResponse,
    InstagramTrackingUserResponse,
)

from ...orm.database.models import (
    InstagramSessions,
    InstagramTracking,
    InstagramUsers,
)
from ...orm.database.repositories import (
    InstagramSessionRepository,
    InstagramUserRepository,
    InstagramUserStatsRepository,
    InstagramUserPostsRepository,
    InstagramUserRelationsRepository,
    InstagramTrackingRepository,
)


conf: IConfEnv = app_conf()


db = IDatabase(conf)

session_repository = InstagramSessionRepository(
    db,
)


user_repository = InstagramUserRepository(
    db,
)


user_stats_repository = InstagramUserStatsRepository(
    db,
)


user_posts_repository = InstagramUserPostsRepository(
    db,
)


user_relations_repository = InstagramUserRelationsRepository(
    db,
)


user_tracking_repository = InstagramTrackingRepository(
    db,
)


class InstagramCore:
    def __init__(
        self,
        conf: IConfEnv = conf,
    ) -> None:
        self._conf = conf
        self._api = InstagramAPI(
            token=conf.rocket_token,
        )

    def __validate_uuid(
        arg_name: str,
        param: str = "id",
    ):
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                sig = signature(func)
                bound_args = sig.bind(*args, **kwargs)
                bound_args.apply_defaults()

                if arg_name not in bound_args.arguments:
                    raise ValueError(
                        f"Argument '{arg_name}' not found in function call"
                    )

                uuid_value = bound_args.arguments[arg_name]

                # Проверка UUID
                session_uuid = await session_repository.fetch_with_filters(
                    uuid=uuid_value
                )
                if session_uuid is None:
                    raise InstagramError(
                        status_code=400,
                        detail=f"Session with requested uuid: {uuid_value} wasn't found.",
                    )

                kwargs["session_param"] = getattr(
                    session_uuid,
                    param,
                )
                return await func(*args, **kwargs)

            return wrapper

        return decorator

    # async def __update_full_data(
    #     self,
    #     username: str,
    # ):
    #     user = await user_repository.fetch_with_filters(
    #         username=username,
    #     )
    #     if user is None:
    #         try:
    #             user_response = self._api.get_web_profile_info(
    #                 username=username,
    #             )
    #             loaded_response = RocketBodyUser(**user_response)
    #         except BadResponseException as err:
    #             raise err

    #         user: dict[str, Any] = loaded_response.data.get("user", {})

    #         profile = RocketProfile.from_rocket(user)
    #         user_data = profile.model_copy(update={"statistics": None})

    #         await user_repository.add_record(
    #             user_data,
    #         )

    #     user_followers = self.__paginate(self._api.get_user_followers(user.))

    def __paginate(
        self,
        fetch_func: Callable[..., dict[str, Any]],
        user_id: int,
        count: int = 50,
    ) -> Generator[dict[str, Any], None, None]:
        """
        Универсальный пагинатор для Instagram API.
        Возвращает генератор пользователей (followers/following).
        """
        next_max_id: str | None = None
        while True:
            try:
                response = fetch_func(
                    user_id=user_id,
                    count=count,
                    max_id=next_max_id,
                )
            except BadResponseException:
                # 🚫 Нет данных (например, у пользователя нет подписчиков)
                break
            except Exception as err:
                raise RuntimeError(f"Instagram API error: {err}") from err

            users = response.get("users", [])
            if not users:
                # 🚫 Если ответ пустой — просто выходим
                break

            for user in users:
                yield user

            next_max_id = response.get("next_max_id")
            if not next_max_id:
                break

    def __get_user_info(
        self,
        indetificator: str | int,
        is_username: bool = True,
        find_method: bool = True,
    ):
        try:
            if not is_username:
                response = self._api.get_user_info_by_id(
                    user_id=indetificator,
                )
            else:
                response = self._api.get_user_info(
                    username=indetificator,
                )
        except (BadResponseException, Exception):
            raise InstagramError.from_exception(
                ProfileNotExistsException,
            )
        if not find_method:
            loaded_response = IRocketBodyUser(**response)

            return loaded_response.user

        loaded_response = RocketBodyUser(**response)

        return loaded_response.data.get("user", {})

    async def __update_user_stats(
        self,
        session: ISession | None = None,
        uuid: str | None = None,
        user_id: str = None,
    ):
        if session is None:
            session_data = await session_repository.fetch_with_filters(
                uuid=uuid,
            )

            session = ISession.model_validate(session_data)

        user = await self.__update_user_data(
            session.ds_user_id if user_id is None else user_id,
        )

        likes, comments, publications = await self.__update_user_posts(
            session.ds_user_id if user_id is None else user_id,
        )

        (
            followers,
            following,
            mutual,
            non_following,
            non_followers,
        ) = await self.__fetch_user_relations(
            session.ds_user_id if user_id is None else user_id,
        )

        await self.__update_user_posts(
            user_id=user_id,
        )

        user_stats = await user_stats_repository.fetch_with_filters(
            user_id=user.id,
            created_at=now().date(),
        )

        if user_id is not None:
            tracking_data = UserTracking(
                target_user_id=user.id,
                owner_user_id=session_data.user_id,
            )

            tracking = await user_tracking_repository.fetch_with_filters(
                target_user_id=user.id,
                owner_user_id=session_data.user_id,
            )

            if tracking is None:
                await user_tracking_repository.add_record(
                    tracking_data,
                )

            tracking = await user_tracking_repository.fetch_with_filters(
                target_user_id=user.id,
                owner_user_id=session_data.user_id,
            )

        stats_data = self.__generate_stats(
            user.id,
            likes,
            comments,
            publications,
            followers,
            following,
            mutual,
            non_following,
            non_followers,
            tracking.id if user_id is not None else None,
        )

        if user_stats is None:
            await user_stats_repository.add_record(
                stats_data,
            )

        return user

    def __generate_stats(
        self,
        user_id: int,
        likes_count: int,
        comments_count: int,
        publications_count: int,
        followers_count: int,
        following_count: int,
        mutual_subscriptions_count: int,
        non_reciprocal_followers_count: int,
        non_reciprocal_following_count: int,
        tracking_id: int | None = None,
    ) -> InstagramUserStatistics:
        return InstagramUserStatistics(
            user_id=user_id,
            likes_count=likes_count,
            comments_count=comments_count,
            publications_count=publications_count,
            followers_count=followers_count,
            following_count=following_count,
            mutual_subscriptions_count=mutual_subscriptions_count,
            non_reciprocal_followers_count=non_reciprocal_followers_count,
            non_reciprocal_following_count=non_reciprocal_following_count,
            tracking_id=tracking_id,
        )

    async def __fetch_user_relations(
        self,
        user_id: int,
    ):
        user = await user_repository.fetch_with_filters(user_id=user_id)

        followers_objs = []
        following_objs = []

        # Сохраняем followers/following в базу
        for relation_type, api_method, container in [
            ("follower", self._api.get_user_followers, followers_objs),
            ("following", self._api.get_user_following, following_objs),
        ]:
            raw_list = self.__paginate(api_method, user_id)
            for item in raw_list:
                follower_data = InstagramFollower(
                    **item, relation_type=relation_type, user_id=user.id
                )
                exists = await user_relations_repository.fetch_with_filters(
                    user_id=user.id, related_username=follower_data.username
                )
                if exists is None:
                    await user_relations_repository.add_record(follower_data)
                container.append(follower_data)

        # Создаем словари для вычислений множеств (ключ — username, значение — полный объект)
        followers_dict = {f.username: f for f in followers_objs}
        following_dict = {f.username: f for f in following_objs}

        # Вычисляем категории
        mutual_usernames = set(followers_dict.keys()) & set(following_dict.keys())
        not_following_back_usernames = set(following_dict.keys()) - set(
            followers_dict.keys()
        )
        not_followed_by_usernames = set(followers_dict.keys()) - set(
            following_dict.keys()
        )

        # Функция для сохранения категорий в базу
        async def save_category(usernames, source_dict, relation_type):
            for username in usernames:
                exists = await user_relations_repository.fetch_with_filters(
                    user_id=user.id,
                    related_username=username,
                    relation_type=relation_type,
                )
                if exists is None:
                    record = source_dict[username].copy(
                        update={"relation_type": relation_type}
                    )
                    await user_relations_repository.add_record(record)

        await save_category(
            mutual_usernames,
            followers_dict,
            "mutual",
        )
        await save_category(
            not_following_back_usernames,
            following_dict,
            "not_following_back",
        )
        await save_category(
            not_followed_by_usernames,
            followers_dict,
            "not_followed_by",
        )

        # Возвращаем как раньше
        return (
            len(followers_objs),
            len(following_objs),
            len(mutual_usernames),
            len(not_following_back_usernames),
            len(not_followed_by_usernames),
        )

    async def __update_user_data(
        self,
        user_id: int,
    ):
        async def call(
            user_id: int,
        ):
            return await user_repository.fetch_with_filters(
                user_id=user_id,
            )

        user_data = await call(user_id)

        if user_data is None:
            user = self.__get_user_info(
                user_id,
                is_username=False,
                find_method=False,
            )

            user_data = IRocketProfile.from_rocket(user)

            await user_repository.add_record(
                user_data,
            )

        user_data = await call(user_id)

        return user_data

    async def __update_user_posts(
        self,
        user_id: int,
    ):
        user = await user_repository.fetch_with_filters(
            user_id=user_id,
        )
        try:
            response = self._api.get_user_media(
                user_id=user_id,
                count=12,
            )
            loaded_response = RocketBodyMedia(**response)
        except (BadResponseException, Exception):
            return (0, 0, 0)

        posts = list(
            map(
                lambda post: InstagramPost.from_rocket(
                    post,
                    user_id=user.id,
                ),
                loaded_response.items,
            ),
        )

        for post in posts:
            user_post = await user_posts_repository.fetch_with_filters(
                user_id=user.id,
                post_url=post.post_url,
            )
            if user_post is None:
                await user_posts_repository.add_record(
                    post,
                )

        likes_count = sum(map(lambda post: post.likes_count, posts))

        comments_count = sum(map(lambda post: post.comments_count, posts))

        publications_count = len(posts)

        return (likes_count, comments_count, publications_count)

    async def save_user_session(
        self,
        session: ISession,
    ) -> InstagramAuthResponse:
        user_session = await session_repository.fetch_with_filters(
            sessionid=session.sessionid
        )

        if user_session is not None:
            user_uuid = user_session.uuid

        if user_session is None:
            user = await self.__update_user_stats(
                session=session,
            )

            try:
                session_data = AddSession(
                    user_id=user.id,
                    **session.dict,
                )

                user_uuid = session_data.uuid

                await session_repository.add_record(
                    session_data,
                )
            except Exception as err:
                raise err

        return InstagramAuthResponse(
            uuid=user_uuid,
        )

    @__validate_uuid("uuid")
    async def find_user(
        self,
        uuid: str,
        username: str,
        session_param: int | None = None,
    ) -> SearchUser:
        user_data = await user_repository.fetch_one_to_many(
            "username",
            username,
            many=False,
            related=["statistics"],
        )
        if user_data is None:
            user = self.__get_user_info(
                username,
                is_username=True,
            )

            user_data = RocketProfile.from_rocket(user)

        return SearchUser.model_validate(user_data)

    @__validate_uuid("uuid")
    async def add_user_tracking(
        self,
        uuid: str,
        user_id: int,
        session_param: int | None = None,
    ) -> InstagramTrackingUserResponse:
        try:
            await self.__update_user_stats(
                uuid=uuid,
                user_id=user_id,
            )
        except BadResponseException as err:
            raise err

        return InstagramTrackingUserResponse(
            uuid=uuid,
        )

    @__validate_uuid("uuid", "user_id")
    async def fetch_subscribers(
        self,
        uuid: str,
        relation_type: str,
        session_param: int | None = None,
    ):
        user_session: InstagramSessions = await session_repository.fetch_with_filters(
            uuid=uuid,
        )

        async def call(
            user_id: int,
        ):
            created_at = date.today() if relation_type == "new" else None
            return await user_relations_repository.fetch_with_filters(
                user_id=user_id,
                many=True,
                relation_type="unsub" if relation_type == "unsub" else "follower",
                created_at=created_at,
            )

        user_subscribers = await call(session_param)

        if len(user_subscribers) <= 0 and relation_type == "new":
            subscribers = self.__paginate(
                self._api.get_user_followers,
                user_session.ds_user_id,
            )

            for subscriber in subscribers:
                subscriber_data = InstagramFollower(
                    **subscriber,
                    user_id=session_param,
                    relation_type="follower",
                )

                await user_relations_repository.add_record(
                    subscriber_data,
                )

        user_subscribers = await call(session_param)

        return list(
            map(
                lambda subscriber: InstagramFollower.model_validate(
                    subscriber,
                ),
                user_subscribers,
            )
        )

    @__validate_uuid("uuid", "user_id")
    async def fetch_subscribtions(
        self,
        uuid: str,
        relation_type: str,
        session_param: int | None = None,
    ):
        user_session: InstagramSessions = await session_repository.fetch_with_filters(
            uuid=uuid,
        )

        async def call(
            user_id: int,
        ):
            return await user_relations_repository.fetch_with_filters(
                user_id=user_id,
                many=True,
                relation_type=relation_type,
            )

        user_subscribtions = await call(session_param)

        if len(user_subscribtions) <= 0:
            subscribtions = self.__paginate(
                self._api.get_user_following,
                user_session.ds_user_id,
            )

            for subscribtion in subscribtions:
                subscriber_data = InstagramFollower(
                    **subscribtion,
                    user_id=session_param,
                    relation_type="following",
                )

                await user_relations_repository.add_record(
                    subscriber_data,
                )

        user_subscribers = await call(session_param)

        return list(
            map(
                lambda subscriber: InstagramFollower.model_validate(
                    subscriber,
                ),
                user_subscribers,
            )
        )

    @__validate_uuid("uuid")
    async def update_user_data(
        self,
        uuid: str,
        session_param: int | None = None,
    ) -> InstagramUpdateUserResponse:
        await self.__update_user_stats(
            uuid=uuid,
        )
        return InstagramUpdateUserResponse(
            uuid=uuid,
        )

    async def fetch_tracking_subscribers(
        self,
        username: str,
        relation_type: str,
    ):
        user: InstagramUsers = await user_repository.fetch_with_filters(
            username=username,
        )

        async def call(
            user_id: int,
        ):
            created_at = date.today() if relation_type == "new" else None
            return await user_relations_repository.fetch_with_filters(
                user_id=user_id,
                many=True,
                relation_type="unsub" if relation_type == "unsub" else "follower",
                created_at=created_at,
            )

        user_subscribers = await call(user.id)

        if len(user_subscribers) <= 0 and relation_type == "new":
            subscribers = self.__paginate(
                self._api.get_user_followers,
                user.user_id,
            )

            for subscriber in subscribers:
                subscriber_data = InstagramFollower(
                    **subscriber,
                    user_id=user.id,
                    relation_type="follower",
                )

                await user_relations_repository.add_record(
                    subscriber_data,
                )

            user_subscribers = await call(user.id)

        return list(
            map(
                lambda subscriber: InstagramFollower.model_validate(
                    subscriber,
                ),
                user_subscribers,
            )
        )

    async def fetch_tracking_subscribtions(
        self,
        username: str,
    ):
        user: InstagramUsers = await user_repository.fetch_with_filters(
            username=username,
        )

        async def call(
            user_id: int,
        ):
            return await user_relations_repository.fetch_with_filters(
                user_id=user_id,
                many=True,
                relation_type=relation_type,
            )

        user_subscribtions = await call(user.id)

        if len(user_subscribtions) <= 0:
            subscribtions = self.__paginate(
                self._api.get_user_following,
                user.user_id,
            )

            for subscribtion in subscribtions:
                subscriber_data = InstagramFollower(
                    **subscribtion,
                    user_id=user.id,
                    relation_type="following",
                )

                await user_relations_repository.add_record(
                    subscriber_data,
                )

            user_subscribers = await call(user.id)

        return list(
            map(
                lambda subscriber: InstagramFollower.model_validate(
                    subscriber,
                ),
                user_subscribers,
            )
        )


class InstagramGPTCore(HttpClient):
    """Базовый клиент для работы с PixVerse API.

    Наследует функциональность Web3 клиента и добавляет специализированные методы
    для взаимодействия с PixVerse API. Автоматически использует базовый URL сервиса.

    Args:
        headers (dict[str, Any]): Заголовки HTTP-запросов (должен содержать JWT)
    """

    def __init__(
        self,
    ) -> None:
        """Инициализация клиента PixVerse.

        Args:
            headers (dict): Заголовки запросов, обязательно включающие:
                - 'Token': Ключ авторизации
        """
        super().__init__(
            CHATGPT_API_URL,  # Базовый URL из конфигурации
        )

    async def post(
        self,
        token: str = None,
        *args,
        **kwargs,
    ) -> ChatGPTInstagramResponse | ChatGPTErrorResponse:
        """Отправка POST-запроса к PixVerse API.

        Args:
            *args: Позиционные аргументы для send_request:
                - endpoint (str): Конечная точка API
                - body (ISchema, optional): Тело запроса
            **kwargs: Именованные аргументы для send_request

        Returns:
            dict[str, Any]: Ответ API в формате JSON

        """
        try:
            response: dict[str, Any] = await super().send_request(
                RequestMethod.POST,
                headers=IAuthHeaders(
                    token=token,
                )
                if token is not None
                else None,
                timeout=90,
                *args,
                **kwargs,
            )
            if not response.get("error"):
                return ChatGPTInstagramResponse(**response)
            return ChatGPTErrorResponse(**response)
        except HTTPError as err:
            if err.response is not None:
                try:
                    error_json = err.response.json()
                    return ChatGPTErrorResponse(**error_json)
                except Exception as json_err:
                    raise json_err
            raise HTTPException(status_code=502, detail=str(err))

    async def get(
        self,
        token: str = None,
        *args,
        **kwargs,
    ) -> ChatGPTInstagramResponse | ChatGPTErrorResponse:
        """Отправка GET-запроса к PixVerse API.

        Args:
            *args: Позиционные аргументы для send_request:
                - endpoint (str): Конечная точка API
            **kwargs: Именованные аргументы для send_request

        Returns:
            dict[str, Any]: Ответ API в формате JSON

        """
        try:
            response: dict[str, Any] = await super().send_request(
                RequestMethod.GET,
                headers=IAuthHeaders(
                    token=token,
                )
                if token is not None
                else None,
                timeout=90,
                *args,
                **kwargs,
            )
            if not response.get("error"):
                return ChatGPTInstagramResponse(**response)
            return ChatGPTErrorResponse(**response)
        except HTTPError as err:
            if err.response is not None:
                try:
                    error_json = err.response.json()
                    return ChatGPTErrorResponse(**error_json)
                except Exception as json_err:
                    raise json_err
            raise HTTPException(status_code=502, detail=str(err))
