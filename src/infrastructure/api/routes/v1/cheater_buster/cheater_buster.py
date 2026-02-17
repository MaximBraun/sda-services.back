# coding utf-8

from fastapi import (
    APIRouter,
    UploadFile,
    Request,
    Query,
)

from PicImageSearch import Network, Yandex

from PicImageSearch.model import YandexResponse

from ......domain.tools import (
    check_user_tokens,
)


from ......interface.schemas.external import LocationResponse


cheater_buster_router = APIRouter(tags=["Cheater Buster"])


@cheater_buster_router.post(
    "/photo2location",
    response_model=list[LocationResponse],
    response_model_exclude_none=True,
)
@check_user_tokens(method_cost=5)
async def photo_to_location(
    request: Request,
    image: UploadFile,
    app_id: str = Query(alias="appId"),
    user_id: str = Query(alias="userId"),
) -> list[LocationResponse]:
    file_bytes = await image.read()
    async with Network() as client:
        yandex = Yandex(client=client)

        resp: YandexResponse = await yandex.search(
            file=file_bytes,
        )

        data = map(
            lambda item: LocationResponse(
                title=item.title,
                source_url=item.url,
                image_url=item.thumbnail,
            ),
            resp.raw,
        )

        return list(data)
