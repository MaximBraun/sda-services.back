# coding utf-8

from ...models import InstagramUserPosts

from ......domain.repositories import (
    IDatabase,
    DatabaseRepository,
)


class InstagramUserPostsRepository(DatabaseRepository):
    def __init__(
        self,
        engine: IDatabase,
    ) -> None:
        super().__init__(
            engine,
            InstagramUserPosts,
        )
