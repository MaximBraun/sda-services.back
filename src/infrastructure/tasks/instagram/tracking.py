# coding utf-8

from typing import Any

from .core import InstagramCelery


class InstagramTrackingCelery(InstagramCelery):
    def __init__(self) -> None:
        super().__init__()

    async def update_tracking_data(
        self,
    ) -> Any:
        return await self.client.update_all_tracked_users_data()
