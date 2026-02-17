# # coding utf-8

from fastapi_pagination import Page

from ......interface.controllers.api.v1 import InstagramController

from ......domain.entities.instagram import ISession

from ......interface.schemas.external import (
    IInstagramUser,
    ITrackingUser,
    InstagramAuthResponse,
    InstagramUserResponse,
    InstagramUpdateUserResponse,
    InstagramTrackingUserResponse,
    InstagramFollower,
    InstagramPost,
    ChatGPTInstagram,
    ChartData,
)

from ......interface.schemas.api import SearchUser


class InstagramView:
    def __init__(
        self,
        controller: InstagramController,
    ) -> None:
        self._controller = controller

    async def auth_user_session(
        self,
        body: ISession,
    ) -> InstagramAuthResponse:
        return await self._controller.auth_user_session(
            body,
        )

    async def update_user_data(
        self,
        body: IInstagramUser,
        uuid: str,
    ) -> InstagramUpdateUserResponse:
        return await self._controller.update_user_data(
            body,
            uuid,
        )

    async def find_user(
        self,
        uuid: str,
        username: str,
    ) -> SearchUser:
        return await self._controller.find_user(
            uuid,
            username,
        )

    async def add_user_tracking(
        self,
        uuid: str,
        user_id: int,
    ) -> InstagramTrackingUserResponse:
        return await self._controller.add_user_tracking(
            uuid,
            user_id,
        )

    async def remove_user_tracking(
        self,
        uuid: str,
        user_id: int,
    ) -> bool:
        return await self._controller.remove_user_tracking(
            uuid,
            user_id,
        )

    async def fetch_user_tracking(
        self,
        uuid: str,
    ) -> Page[ITrackingUser]:
        return await self._controller.fetch_user_tracking(
            uuid,
        )

    async def fetch_statistics(
        self,
        body: IInstagramUser,
        uuid: str,
    ) -> InstagramUserResponse:
        return await self._controller.fetch_statistics(
            body,
            uuid,
        )

    async def fetch_publication(
        self,
        body: IInstagramUser,
        uuid: str,
        id: int,
    ) -> InstagramPost:
        return await self._controller.fetch_publication(
            body,
            uuid,
            id,
        )

    async def fetch_tracking_publication(
        self,
        body: IInstagramUser,
        username: str,
        id: int,
    ) -> InstagramPost:
        return await self._controller.fetch_tracking_publication(
            body,
            username,
            id,
        )

    async def fetch_subscribers(
        self,
        body: IInstagramUser,
        uuid: str,
        relation_type: str,
    ) -> Page[InstagramFollower]:
        return await self._controller.fetch_subscribers(
            body,
            uuid,
            relation_type,
        )

    async def fetch_tracking_subscribers(
        self,
        body: IInstagramUser,
        username: str,
        relation_type: str,
    ) -> Page[InstagramFollower]:
        return await self._controller.fetch_tracking_subscribers(
            body,
            username,
            relation_type,
        )

    async def fetch_secret_fans(
        self,
        body: IInstagramUser,
        uuid: str,
    ) -> Page[InstagramFollower]:
        return await self._controller.fetch_secret_fans(
            body,
            uuid,
        )

    async def fetch_tracking_secret_fans(
        self,
        body: IInstagramUser,
        username: str,
    ) -> Page[InstagramFollower]:
        return await self._controller.fetch_tracking_secret_fans(
            body,
            username,
        )

    async def fetch_subscribtions(
        self,
        body: IInstagramUser,
        uuid: str,
        relation_type: str,
    ) -> Page[InstagramFollower]:
        return await self._controller.fetch_subscribtions(
            body,
            uuid,
            relation_type,
        )

    async def fetch_tracking_subscribtions(
        self,
        body: IInstagramUser,
        username: str,
        relation_type: str,
    ) -> Page[InstagramFollower]:
        return await self._controller.fetch_tracking_subscribtions(
            body,
            username,
            relation_type,
        )

    async def image_to_post(
        self,
        uuid: str,
        body: IInstagramUser,
    ) -> ChatGPTInstagram:
        return await self._controller.image_to_post(
            uuid,
            body,
        )

    async def user_subscribers_chart(
        self,
        uuid: str,
        body: IInstagramUser,
    ) -> Page[ChartData]:
        return await self._controller.user_subscribers_chart(
            uuid,
            body,
        )

    async def fetch_public_statistics(
        self,
        body: IInstagramUser,
        username: str,
    ) -> Page[ChartData]:
        return await self._controller.fetch_public_statistics(
            body,
            username,
        )

    async def tracking_user_subscribers_chart(
        self,
        body: IInstagramUser,
        username: str,
    ) -> Page[InstagramFollower]:
        return await self._controller.tracking_user_subscribers_chart(
            body,
            username,
        )
